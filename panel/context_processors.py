from website.models import ContactSubmission


def panel_sidebar(request):
    if not request.path.startswith('/panel') or not request.user.is_authenticated:
        return {}
    return {
        'unread_contacts': ContactSubmission.objects.filter(is_read=False).count(),
    }
