from django.contrib import admin
from django.utils.html import format_html
from django_summernote.admin import SummernoteModelAdmin

from website.models import (
    BlogPost,
    ContactSubmission,
    ContentPage,
    PageAssessmentStep,
    PageCaseStudy,
    PageContentBenefit,
    PageContentFAQ,
    PageContentSection,
    PageRecoveryPhase,
    PageTreatmentMethod,
    PatientDocument,
)


class PageContentSectionInline(admin.TabularInline):
    model = PageContentSection
    extra = 1
    fields = ('sort_order', 'heading', 'body')
    ordering = ('sort_order', 'id')


class PageContentBenefitInline(admin.TabularInline):
    model = PageContentBenefit
    extra = 1
    fields = ('sort_order', 'text')
    ordering = ('sort_order', 'id')


class PageContentFAQInline(admin.TabularInline):
    model = PageContentFAQ
    extra = 1
    fields = ('sort_order', 'question', 'answer')
    ordering = ('sort_order', 'id')


class PageAssessmentStepInline(admin.TabularInline):
    model = PageAssessmentStep
    extra = 1
    fields = ('sort_order', 'title', 'body')
    ordering = ('sort_order', 'id')


class PageTreatmentMethodInline(admin.TabularInline):
    model = PageTreatmentMethod
    extra = 1
    fields = ('sort_order', 'title', 'body')
    ordering = ('sort_order', 'id')


class PageRecoveryPhaseInline(admin.TabularInline):
    model = PageRecoveryPhase
    extra = 1
    fields = ('sort_order', 'phase', 'timeframe', 'body')
    ordering = ('sort_order', 'id')


class PageCaseStudyInline(admin.TabularInline):
    model = PageCaseStudy
    extra = 1
    fields = ('sort_order', 'patient_label', 'issue', 'timeline', 'approach', 'outcome')
    ordering = ('sort_order', 'id')


@admin.register(ContentPage)
class ContentPageAdmin(SummernoteModelAdmin):
    summernote_fields = ('description',)
    list_display = ('title', 'section', 'slug', 'image_preview', 'is_published', 'sort_order', 'updated_at')
    list_filter = ('section', 'is_published', 'is_primary', 'menu_column')
    search_fields = ('title', 'slug', 'summary', 'meta_description')
    prepopulated_fields = {'slug': ('title',)}
    inlines = (
        PageAssessmentStepInline,
        PageTreatmentMethodInline,
        PageRecoveryPhaseInline,
        PageCaseStudyInline,
        PageContentSectionInline,
        PageContentBenefitInline,
        PageContentFAQInline,
    )
    fieldsets = (
        (None, {
            'fields': (
                'section',
                'title',
                'slug',
                'summary',
                'image',
                'image_alt',
                'is_published',
            ),
        }),
        ('Page content', {
            'fields': (
                'description',
                'benefits_heading',
                'faq_intro',
            ),
        }),
        ('Treatment quick stats', {
            'fields': (
                'typical_sessions',
                'first_improvement',
                'recovery_timeline',
            ),
            'classes': ('collapse',),
        }),
        ('SEO & navigation', {
            'fields': (
                'meta_description',
                'is_primary',
                'menu_column',
                'sort_order',
            ),
        }),
    )

    @admin.display(description='Image')
    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="height:48px;width:72px;object-fit:cover;border-radius:6px;" alt="">',
                obj.image.url,
            )
        return 'No image'


@admin.register(PatientDocument)
class PatientDocumentAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'file_extension_display', 'is_published', 'sort_order', 'updated_at')
    list_filter = ('category', 'is_published')
    search_fields = ('title', 'slug', 'description')
    prepopulated_fields = {'slug': ('title',)}
    ordering = ('sort_order', 'title')
    fieldsets = (
        (None, {
            'fields': ('title', 'slug', 'description', 'category', 'is_published', 'sort_order'),
        }),
        ('File', {
            'fields': ('file', 'static_file'),
            'description': 'Upload a file or provide a path under static/ (e.g. documents/form.pdf).',
        }),
    )

    @admin.display(description='Type')
    def file_extension_display(self, obj):
        return obj.file_extension


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'published_date', 'is_published', 'updated_at')
    list_filter = ('is_published', 'tag')
    search_fields = ('title', 'slug', 'summary', 'meta_description')
    prepopulated_fields = {'slug': ('title',)}
    ordering = ('-published_date', '-created_at')


@admin.register(ContactSubmission)
class ContactSubmissionAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'phone', 'is_read', 'created_at')
    list_filter = ('is_read', 'created_at')
    search_fields = ('first_name', 'last_name', 'email', 'phone', 'message')
    readonly_fields = ('created_at',)
    ordering = ('-created_at',)
