from datetime import datetime, time

from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.views import LoginView, LogoutView
from django.db.models import Max
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.views.decorators.http import require_GET, require_http_methods, require_POST

from bookings.models import Appointment, Service, ServiceSchedule
from panel.decorators import staff_required
from panel.forms import (
    BlogPostForm,
    PanelLoginForm,
    StaffUserCreateForm,
    StaffUserForm,
)
from website.models import BlogPost, ContactSubmission
from website.services.blog import backfill_blog_content_from_sections, sync_legacy_blog_posts
from website.visit import clinic_hours_bounds, clinic_hours_label

User = get_user_model()

STATUS_COLORS = {
    'pending': '#f59e0b',
    'confirmed': '#009989',
    'cancelled': '#94a3b8',
    'completed': '#1B367E',
    'no_show': '#ef4444',
}

DEFAULT_START = time(8, 0)
DEFAULT_END = time(17, 30)


def _parse_time_field(value):
    if not value:
        return None
    try:
        return datetime.strptime(value, '%H:%M').time()
    except ValueError:
        return None


def _weekly_schedule_rows(service):
    existing = {row.day_of_week: row for row in service.schedules.all()}
    rows = []
    for day_value, day_label in ServiceSchedule.DayOfWeek.choices:
        row = existing.get(day_value)
        clinic_opens, clinic_closes = clinic_hours_bounds(day_value)
        default_start = clinic_opens or DEFAULT_START
        default_end = clinic_closes or DEFAULT_END
        rows.append({
            'day_value': day_value,
            'day_label': day_label,
            'start_time': (
                row.start_time.strftime('%H:%M')
                if row and row.start_time else default_start.strftime('%H:%M')
            ),
            'end_time': (
                row.end_time.strftime('%H:%M')
                if row and row.end_time else default_end.strftime('%H:%M')
            ),
            'is_unavailable': row.is_unavailable if row else False,
            'clinic_opens': clinic_opens.strftime('%H:%M') if clinic_opens else '',
            'clinic_closes': clinic_closes.strftime('%H:%M') if clinic_closes else '',
            'clinic_hours_label': clinic_hours_label(day_value),
        })
    return rows


def _save_weekly_schedule(service, post_data):
    for day_value, day_label in ServiceSchedule.DayOfWeek.choices:
        prefix = f'day_{day_value}'
        is_unavailable = post_data.get(f'{prefix}_unavailable') == 'on'
        start_time = None if is_unavailable else _parse_time_field(post_data.get(f'{prefix}_start'))
        end_time = None if is_unavailable else _parse_time_field(post_data.get(f'{prefix}_end'))

        if not is_unavailable:
            if not start_time or not end_time or start_time >= end_time:
                return False, f'{day_label}: enter a valid start and end time.'

            clinic_opens, clinic_closes = clinic_hours_bounds(day_value)
            if clinic_opens is None or clinic_closes is None:
                return False, f'{day_label}: the clinic is closed — mark this day as unavailable.'

            if start_time < clinic_opens:
                return False, (
                    f'{day_label}: start time cannot be before clinic opening '
                    f'({clinic_hours_label(day_value)}).'
                )
            if end_time > clinic_closes:
                return False, (
                    f'{day_label}: end time cannot be after clinic closing '
                    f'({clinic_hours_label(day_value)}).'
                )

        ServiceSchedule.objects.update_or_create(
            service=service,
            day_of_week=day_value,
            defaults={
                'is_unavailable': is_unavailable,
                'start_time': start_time,
                'end_time': end_time,
            },
        )
    return True, None


class PanelLoginView(LoginView):
    template_name = 'panel/login.html'
    authentication_form = PanelLoginForm
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse('panel:dashboard')


class PanelLogoutView(LogoutView):
    next_page = reverse_lazy('panel:login')


@staff_required
def dashboard(request):
    today = timezone.localdate()
    upcoming = Appointment.objects.filter(
        start_datetime__date__gte=today,
        status__in=[Appointment.Status.PENDING, Appointment.Status.CONFIRMED],
    ).select_related('customer', 'service').order_by('start_datetime')[:8]

    stats = {
        'today_count': Appointment.objects.filter(
            start_datetime__date=today,
            status__in=[Appointment.Status.PENDING, Appointment.Status.CONFIRMED],
        ).count(),
        'unread_contacts': ContactSubmission.objects.filter(is_read=False).count(),
        'published_posts': BlogPost.objects.filter(is_published=True).count(),
        'active_services': Service.objects.filter(is_active=True).count(),
    }

    return render(request, 'panel/dashboard.html', {
        'page_title': 'Dashboard',
        'upcoming': upcoming,
        'stats': stats,
    })


@staff_required
@require_GET
def appointments_api(request):
    start_param = request.GET.get('start')
    end_param = request.GET.get('end')
    since_param = request.GET.get('since')

    queryset = Appointment.objects.select_related('customer', 'service', 'practitioner')

    if start_param and end_param:
        try:
            start = datetime.fromisoformat(start_param.replace('Z', '+00:00'))
            end = datetime.fromisoformat(end_param.replace('Z', '+00:00'))
            if timezone.is_naive(start):
                start = timezone.make_aware(start)
            if timezone.is_naive(end):
                end = timezone.make_aware(end)
            queryset = queryset.filter(start_datetime__gte=start, start_datetime__lt=end)
        except ValueError:
            pass

    if since_param:
        try:
            since = datetime.fromisoformat(since_param.replace('Z', '+00:00'))
            if timezone.is_naive(since):
                since = timezone.make_aware(since)
            queryset = queryset.filter(updated_at__gte=since)
        except ValueError:
            pass

    events = []
    for appointment in queryset.order_by('start_datetime'):
        events.append({
            'id': appointment.pk,
            'title': f'{appointment.service.name} — {appointment.customer.full_name}',
            'start': timezone.localtime(appointment.start_datetime).isoformat(),
            'end': timezone.localtime(appointment.end_datetime).isoformat(),
            'backgroundColor': STATUS_COLORS.get(appointment.status, '#009989'),
            'borderColor': STATUS_COLORS.get(appointment.status, '#009989'),
            'extendedProps': {
                'status': appointment.status,
                'phone': appointment.customer.phone,
                'email': appointment.customer.email,
                'service': appointment.service.name,
                'notes': appointment.customer_notes,
                'updated_at': appointment.updated_at.isoformat(),
            },
        })

    latest = Appointment.objects.aggregate(latest=Max('updated_at'))['latest']
    return JsonResponse({
        'events': events,
        'server_time': timezone.now().isoformat(),
        'latest_update': latest.isoformat() if latest else None,
    })


@staff_required
def blog_list(request):
    if not BlogPost.objects.exists():
        sync_legacy_blog_posts()
    else:
        backfill_blog_content_from_sections()
    posts = BlogPost.objects.order_by('-published_date', '-created_at')
    return render(request, 'panel/blog_list.html', {
        'page_title': 'Blog Posts',
        'posts': posts,
    })


@staff_required
@require_http_methods(['GET', 'POST'])
def blog_create(request):
    form = BlogPostForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('panel:blog-list')
    return render(request, 'panel/blog_form.html', {
        'page_title': 'New Blog Post',
        'form': form,
        'is_create': True,
    })


@staff_required
@require_http_methods(['GET', 'POST'])
def blog_edit(request, pk):
    post = get_object_or_404(BlogPost, pk=pk)
    if not (post.content or '').strip() and post.sections:
        backfill_blog_content_from_sections()
        post.refresh_from_db()
    form = BlogPostForm(request.POST or None, instance=post)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('panel:blog-list')
    return render(request, 'panel/blog_form.html', {
        'page_title': f'Edit: {post.title}',
        'form': form,
        'post': post,
        'is_create': False,
    })


@staff_required
@require_POST
def blog_delete(request, pk):
    post = get_object_or_404(BlogPost, pk=pk)
    post.delete()
    return redirect('panel:blog-list')


@staff_required
@require_http_methods(['GET', 'POST'])
def schedules(request):
    services = Service.objects.filter(is_active=True).order_by('sort_order', 'name')
    selected_id = request.GET.get('service') or request.POST.get('service')
    selected = services.filter(pk=selected_id).first() if selected_id else services.first()

    weekday_rows = []
    if selected:
        if request.method == 'POST':
            saved, error = _save_weekly_schedule(selected, request.POST)
            if saved:
                messages.success(request, f'Saved schedule for {selected.name}.')
                return redirect(f'{reverse("panel:schedules")}?service={selected.pk}')
            messages.error(request, error or 'Could not save schedule.')
        weekday_rows = _weekly_schedule_rows(selected)

    return render(request, 'panel/schedules.html', {
        'page_title': 'Service Schedules',
        'services': services,
        'selected_service': selected,
        'weekday_rows': weekday_rows,
    })


@staff_required
def contacts(request):
    submissions = ContactSubmission.objects.order_by('-created_at')
    unread = submissions.filter(is_read=False).count()
    return render(request, 'panel/contacts.html', {
        'page_title': 'Contact Messages',
        'submissions': submissions,
        'unread_count': unread,
    })


@staff_required
@require_http_methods(['GET', 'POST'])
def contact_detail(request, pk):
    submission = get_object_or_404(ContactSubmission, pk=pk)
    if request.method == 'POST':
        submission.is_read = request.POST.get('is_read') == 'on'
        submission.save(update_fields=['is_read'])
        return redirect('panel:contacts')
    if not submission.is_read:
        submission.is_read = True
        submission.save(update_fields=['is_read'])
    return render(request, 'panel/contact_detail.html', {
        'page_title': f'Message from {submission.full_name}',
        'submission': submission,
    })


@staff_required
def users_list(request):
    users = User.objects.filter(is_staff=True).order_by('username')
    return render(request, 'panel/users.html', {
        'page_title': 'Panel Users',
        'users': users,
    })


@staff_required
@require_http_methods(['GET', 'POST'])
def user_create(request):
    form = StaffUserCreateForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('panel:users')
    return render(request, 'panel/user_form.html', {
        'page_title': 'Add Panel User',
        'form': form,
        'is_create': True,
    })


@staff_required
@require_http_methods(['GET', 'POST'])
def user_edit(request, pk):
    user = get_object_or_404(User, pk=pk, is_staff=True)
    form = StaffUserForm(request.POST or None, instance=user)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('panel:users')
    return render(request, 'panel/user_form.html', {
        'page_title': f'Edit User: {user.username}',
        'form': form,
        'panel_user': user,
        'is_create': False,
    })
