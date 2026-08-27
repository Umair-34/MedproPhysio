from django.db import models
from django.utils.text import slugify

from website.image_optimization import webp_url_for_field


class SectionType(models.TextChoices):
    FOCUS_AREAS = 'focus-areas', 'Focus Areas'
    CONDITIONS = 'conditions', 'Conditions We Treat'
    TREATMENTS = 'treatments', 'Our Treatments'


class ContentPage(models.Model):
    section = models.CharField(max_length=32, choices=SectionType.choices, db_index=True)
    slug = models.SlugField(max_length=120)
    title = models.CharField(max_length=200)
    summary = models.TextField(blank=True, help_text='Short summary for hub listing cards.')
    meta_description = models.TextField(blank=True, help_text='SEO meta description for search engines.')
    description = models.TextField(
        blank=True,
        help_text='Main page introduction and rich content shown at the top of the detail page.',
    )
    image = models.ImageField(
        upload_to='content_pages/%Y/%m/',
        blank=True,
        help_text='Upload a hero image file for the detail page and hub card. JPG or PNG recommended.',
    )
    image_alt = models.CharField(
        max_length=200,
        blank=True,
        help_text='Alt text for the page image. Leave blank to use the page title.',
    )
    typical_sessions = models.CharField(
        max_length=80,
        blank=True,
        help_text='Typical number of sessions (treatments only).',
    )
    first_improvement = models.CharField(
        max_length=80,
        blank=True,
        help_text='When patients often notice improvement (treatments only).',
    )
    recovery_timeline = models.CharField(
        max_length=80,
        blank=True,
        help_text='Typical full recovery timeframe (treatments only).',
    )
    benefits_heading = models.CharField(
        max_length=200,
        default='Why choose our Calgary clinic',
        blank=True,
    )
    faq_intro = models.TextField(blank=True)
    is_primary = models.BooleanField(
        default=False,
        help_text='Highlight on homepage and treatment hub (treatments only).',
    )
    menu_column = models.PositiveSmallIntegerField(
        default=1,
        help_text='Mega menu column: 1 = left, 2 = right.',
    )
    sort_order = models.PositiveIntegerField(default=0)
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['section', 'sort_order', 'title']
        constraints = [
            models.UniqueConstraint(fields=['section', 'slug'], name='unique_content_page_slug'),
        ]
        verbose_name = 'Content page'
        verbose_name_plural = 'Content pages'

    def __str__(self):
        return f'{self.get_section_display()}: {self.title}'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def image_webp_url(self):
        return webp_url_for_field(self.image)

    def to_nav_item(self):
        item = {
            'slug': self.slug,
            'title': self.title,
        }
        if self.summary:
            item['summary'] = self.summary
        if self.is_primary:
            item['primary'] = True
        image_url, image_webp_url, image_alt = self._image_urls()
        if image_url:
            item['image_url'] = image_url
            item['image_webp_url'] = image_webp_url
            item['image_alt'] = image_alt
        if self.typical_sessions:
            item['typical_sessions'] = self.typical_sessions
        if self.recovery_timeline:
            item['recovery_timeline'] = self.recovery_timeline
        return item

    def to_page_dict(self, default_faq_intro=''):
        faqs = [(faq.question, faq.answer) for faq in self.faqs.all()]
        faq_intro = self.faq_intro or (default_faq_intro if faqs else '')
        data = {
            'meta_description': self.meta_description,
            'description': self.description,
            'sections': [(block.heading, block.body) for block in self.content_sections.all()],
            'benefits': [benefit.text for benefit in self.benefit_items.all()],
            'benefits_heading': self.benefits_heading,
            'typical_sessions': self.typical_sessions,
            'first_improvement': self.first_improvement,
            'recovery_timeline': self.recovery_timeline,
            'assessment_steps': [
                (step.title, step.body) for step in self.assessment_steps.all()
            ],
            'treatment_methods': [
                (method.title, method.body) for method in self.treatment_methods.all()
            ],
            'recovery_phases': [
                (phase.phase, phase.timeframe, phase.body)
                for phase in self.recovery_phases.all()
            ],
            'case_studies': [
                {
                    'patient_label': case.patient_label,
                    'issue': case.issue,
                    'approach': case.approach,
                    'outcome': case.outcome,
                    'timeline': case.timeline,
                }
                for case in self.case_studies.all()
            ],
            'faqs': faqs,
            'faq_intro': faq_intro,
        }
        image_url, image_webp_url, image_alt = self._image_urls()
        if image_url:
            data['image_url'] = image_url
            data['image_webp_url'] = image_webp_url
            data['image_alt'] = image_alt
        return data

    def _image_urls(self):
        from website.page_images import static_image_path_for

        static_path = static_image_path_for(self.slug)
        if static_path:
            return static_path, None, self.image_alt or self.title
        if self.image:
            return self.image.url, self.image_webp_url(), self.image_alt or self.title
        return None, None, ''


class PageContentSection(models.Model):
    page = models.ForeignKey(
        ContentPage,
        on_delete=models.CASCADE,
        related_name='content_sections',
    )
    heading = models.CharField(max_length=200)
    body = models.TextField()
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['sort_order', 'id']
        verbose_name = 'Content section'
        verbose_name_plural = 'Content sections'

    def __str__(self):
        return self.heading


class PageContentBenefit(models.Model):
    page = models.ForeignKey(
        ContentPage,
        on_delete=models.CASCADE,
        related_name='benefit_items',
    )
    text = models.CharField(max_length=300)
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['sort_order', 'id']
        verbose_name = 'Benefit'
        verbose_name_plural = 'Benefits'

    def __str__(self):
        return self.text


class PageAssessmentStep(models.Model):
    page = models.ForeignKey(
        ContentPage,
        on_delete=models.CASCADE,
        related_name='assessment_steps',
    )
    title = models.CharField(max_length=200)
    body = models.TextField()
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['sort_order', 'id']
        verbose_name = 'Assessment step'
        verbose_name_plural = 'Assessment steps'

    def __str__(self):
        return self.title


class PageTreatmentMethod(models.Model):
    page = models.ForeignKey(
        ContentPage,
        on_delete=models.CASCADE,
        related_name='treatment_methods',
    )
    title = models.CharField(max_length=200)
    body = models.TextField()
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['sort_order', 'id']
        verbose_name = 'Treatment method'
        verbose_name_plural = 'Treatment methods'

    def __str__(self):
        return self.title


class PageRecoveryPhase(models.Model):
    page = models.ForeignKey(
        ContentPage,
        on_delete=models.CASCADE,
        related_name='recovery_phases',
    )
    phase = models.CharField(max_length=120)
    timeframe = models.CharField(max_length=80)
    body = models.TextField()
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['sort_order', 'id']
        verbose_name = 'Recovery phase'
        verbose_name_plural = 'Recovery phases'

    def __str__(self):
        return f'{self.phase} ({self.timeframe})'


class PageCaseStudy(models.Model):
    page = models.ForeignKey(
        ContentPage,
        on_delete=models.CASCADE,
        related_name='case_studies',
    )
    patient_label = models.CharField(max_length=120)
    issue = models.CharField(max_length=200)
    approach = models.TextField()
    outcome = models.TextField()
    timeline = models.CharField(max_length=80)
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['sort_order', 'id']
        verbose_name = 'Case study'
        verbose_name_plural = 'Case studies'

    def __str__(self):
        return self.patient_label


class PageContentFAQ(models.Model):
    page = models.ForeignKey(
        ContentPage,
        on_delete=models.CASCADE,
        related_name='faqs',
    )
    question = models.CharField(max_length=300)
    answer = models.TextField()
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['sort_order', 'id']
        verbose_name = 'FAQ'
        verbose_name_plural = 'FAQs'

    def __str__(self):
        return self.question


class DocumentCategory(models.TextChoices):
    INTAKE = 'intake', 'Intake forms'
    WCB = 'wcb', 'WCB and workplace'
    INSURANCE = 'insurance', 'Insurance'
    GENERAL = 'general', 'General'


class PatientDocument(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=120, unique=True)
    description = models.TextField(blank=True)
    category = models.CharField(
        max_length=32,
        choices=DocumentCategory.choices,
        default=DocumentCategory.INTAKE,
        db_index=True,
    )
    file = models.FileField(
        upload_to='patient_documents/%Y/%m/',
        blank=True,
        help_text='Upload a PDF or document file. Optional if a bundled static file is set.',
    )
    static_file = models.CharField(
        max_length=255,
        blank=True,
        help_text='Path under static/, e.g. documents/new-patient-intake-form.pdf',
    )
    sort_order = models.PositiveIntegerField(default=0)
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['sort_order', 'title']
        verbose_name = 'Patient document'
        verbose_name_plural = 'Patient documents'

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    @property
    def file_extension(self):
        name = ''
        if self.file:
            name = self.file.name
        elif self.static_file:
            name = self.static_file
        if not name or '.' not in name:
            return 'PDF'
        return name.rsplit('.', 1)[-1].upper()


class BlogPost(models.Model):
    slug = models.SlugField(max_length=120, unique=True)
    title = models.CharField(max_length=200)
    meta_title = models.CharField(max_length=200, blank=True)
    meta_description = models.TextField(blank=True)
    summary = models.TextField()
    tag = models.CharField(max_length=100, blank=True)
    image = models.CharField(
        max_length=255,
        blank=True,
        help_text='Static image path, e.g. images/blog-wcb-workplace-injury.jpg',
    )
    image_alt = models.CharField(max_length=255, blank=True)
    published_date = models.DateField()
    author = models.CharField(max_length=100, default='Medpro Physiotherapy Team')
    reading_time = models.CharField(max_length=30, blank=True, default='5 min read')
    content = models.TextField(
        blank=True,
        help_text='Main article body (HTML). Used when sections JSON is empty.',
    )
    key_takeaways = models.JSONField(default=list, blank=True)
    sections = models.JSONField(default=list, blank=True)
    faqs = models.JSONField(default=list, blank=True)
    related_services = models.JSONField(default=list, blank=True)
    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-published_date', '-created_at']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        if not self.meta_title:
            self.meta_title = self.title
        super().save(*args, **kwargs)

    @property
    def published_display(self):
        return self.published_date.strftime('%B %d, %Y')

    def to_public_dict(self):
        return {
            'slug': self.slug,
            'title': self.title,
            'meta_title': self.meta_title or self.title,
            'meta_description': self.meta_description,
            'summary': self.summary,
            'tag': self.tag,
            'image': self.image or 'images/post-1.jpg',
            'image_alt': self.image_alt or self.title,
            'published_date': self.published_date.isoformat(),
            'published_display': self.published_display,
            'author': self.author,
            'reading_time': self.reading_time,
            'key_takeaways': self.key_takeaways or [],
            'sections': self.sections or [],
            'content': self.content,
            'faqs': self.faqs or [],
            'related_services': self.related_services or [],
        }


class ContactSubmission(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=30, blank=True)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.first_name} {self.last_name} — {self.created_at:%Y-%m-%d}'

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'.strip()
