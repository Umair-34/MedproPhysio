from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from website.content import PATIENT_PAGES
from website.models import BlogPost, ContentPage, SectionType


class StaticViewSitemap(Sitemap):
    _pages = (
        ('website:home', 1.0, 'daily'),
        ('website:services', 0.9, 'weekly'),
        ('website:book', 0.8, 'monthly'),
        ('website:about', 0.7, 'monthly'),
        ('website:visit-us', 0.7, 'monthly'),
        ('website:contact', 0.7, 'monthly'),
        ('website:faqs', 0.6, 'monthly'),
        ('website:blog', 0.7, 'weekly'),
        ('website:patient-stories', 0.6, 'weekly'),
    )

    def items(self):
        return self._pages

    def location(self, item):
        return reverse(item[0])

    def priority(self, item):
        return item[1]

    def changefreq(self, item):
        return item[2]


class ServicePageSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.8

    def items(self):
        return ContentPage.objects.filter(
            section=SectionType.TREATMENTS,
            is_published=True,
        )

    def lastmod(self, obj):
        return obj.updated_at


class BlogPostSitemap(Sitemap):
    changefreq = 'monthly'
    priority = 0.6

    def items(self):
        return BlogPost.objects.filter(is_published=True)

    def lastmod(self, obj):
        return obj.updated_at


class PatientPageSitemap(Sitemap):
    changefreq = 'monthly'
    priority = 0.6

    def items(self):
        return list(PATIENT_PAGES.keys())

    def location(self, slug):
        return reverse('website:patient-page', kwargs={'slug': slug})


SITEMAPS = {
    'static': StaticViewSitemap,
    'services': ServicePageSitemap,
    'blog': BlogPostSitemap,
    'patients': PatientPageSitemap,
}
