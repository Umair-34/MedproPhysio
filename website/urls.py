from django.urls import path
from django.views.generic import RedirectView

from website import views

app_name = 'website'

urlpatterns = [
  path('', views.home, name='home'),
  path('about/', views.about, name='about'),
  path('visit-us/', views.visit_us, name='visit-us'),
  path('contact/', views.contact, name='contact'),
  path('api/contact/', views.contact_submit, name='contact-submit'),
  path('book/', views.book_appointment, name='book'),
  path('faqs/', views.faqs, name='faqs'),
  path('blog/', views.blog, name='blog'),
  path('blog/<slug:slug>/', views.blog_detail, name='blog-detail'),
  path('patient/stories/', views.patient_stories, name='patient-stories'),
  path('patient/<slug:slug>/', views.patient_page, name='patient-page'),
  path(
    'focus-areas/',
    RedirectView.as_view(pattern_name='website:services', permanent=True),
    name='focus-areas',
  ),
  path('focus-areas/<slug:slug>/', views.focus_area_detail_redirect, name='focus-area-detail'),
  path('services/', views.hub, {'section': 'treatments'}, name='services'),
  path('services/<slug:slug>/', views.detail, {'section': 'treatments'}, name='service-detail'),
  path(
    'treatments/',
    RedirectView.as_view(pattern_name='website:services', permanent=True),
    name='treatments',
  ),
  path('treatments/<slug:slug>/', views.legacy_treatment_redirect, name='treatment-detail'),
]

handler404 = 'website.views.page_not_found'
