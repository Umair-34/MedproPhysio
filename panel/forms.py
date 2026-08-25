from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError

from website.models import BlogPost, ContactSubmission
from website.services.blog import sections_to_html

User = get_user_model()


class PanelLoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'panel-input',
            'placeholder': 'Username',
            'autocomplete': 'username',
        }),
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'panel-input',
            'placeholder': 'Password',
            'autocomplete': 'current-password',
        }),
    )

    def confirm_login_allowed(self, user):
        super().confirm_login_allowed(user)
        if not user.is_staff:
            raise ValidationError(
                'This account does not have access to the clinic panel.',
                code='no_panel_access',
            )


class BlogPostForm(forms.ModelForm):
    key_takeaways_text = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'panel-input',
            'rows': 4,
            'placeholder': 'One takeaway per line',
        }),
        label='Key takeaways',
    )

    class Meta:
        model = BlogPost
        fields = [
            'title',
            'slug',
            'summary',
            'tag',
            'image',
            'image_alt',
            'published_date',
            'author',
            'reading_time',
            'meta_title',
            'meta_description',
            'content',
            'is_published',
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'panel-input'}),
            'slug': forms.TextInput(attrs={'class': 'panel-input'}),
            'summary': forms.Textarea(attrs={'class': 'panel-input', 'rows': 3}),
            'tag': forms.TextInput(attrs={'class': 'panel-input'}),
            'image': forms.TextInput(attrs={'class': 'panel-input'}),
            'image_alt': forms.TextInput(attrs={'class': 'panel-input'}),
            'published_date': forms.DateInput(attrs={'class': 'panel-input', 'type': 'date'}),
            'author': forms.TextInput(attrs={'class': 'panel-input'}),
            'reading_time': forms.TextInput(attrs={'class': 'panel-input'}),
            'meta_title': forms.TextInput(attrs={'class': 'panel-input'}),
            'meta_description': forms.Textarea(attrs={'class': 'panel-input', 'rows': 2}),
            # Plain textarea — Summernote is initialized in the blog form template
            # after jQuery loads (django-summernote inplace widgets break when their
            # inline scripts run before jQuery at the bottom of the page).
            'content': forms.Textarea(attrs={
                'class': 'panel-input panel-summernote',
                'rows': 12,
            }),
            'is_published': forms.CheckboxInput(attrs={'class': 'panel-checkbox'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk and self.instance.key_takeaways:
            self.fields['key_takeaways_text'].initial = '\n'.join(self.instance.key_takeaways)
        if self.instance.pk and not self.data:
            if not (self.instance.content or '').strip() and self.instance.sections:
                self.initial['content'] = sections_to_html(self.instance.sections)

    def save(self, commit=True):
        post = super().save(commit=False)
        text = self.cleaned_data.get('key_takeaways_text', '')
        post.key_takeaways = [line.strip() for line in text.splitlines() if line.strip()]
        if (post.content or '').strip():
            post.sections = []
        if commit:
            post.save()
        return post


class StaffUserForm(forms.ModelForm):
    password = forms.CharField(
        required=False,
        widget=forms.PasswordInput(attrs={'class': 'panel-input'}),
        help_text='Leave blank to keep the current password.',
    )

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'is_active', 'is_staff']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'panel-input'}),
            'first_name': forms.TextInput(attrs={'class': 'panel-input'}),
            'last_name': forms.TextInput(attrs={'class': 'panel-input'}),
            'email': forms.EmailInput(attrs={'class': 'panel-input'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'panel-checkbox'}),
            'is_staff': forms.CheckboxInput(attrs={'class': 'panel-checkbox'}),
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_staff = True
        password = self.cleaned_data.get('password')
        if password:
            user.set_password(password)
        if commit:
            user.save()
        return user


class StaffUserCreateForm(StaffUserForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'panel-input'}),
        help_text='Required for new panel users.',
    )

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user


class ContactNoteForm(forms.ModelForm):
    class Meta:
        model = ContactSubmission
        fields = ['is_read']
