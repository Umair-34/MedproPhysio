"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import include, path, re_path
from django.views.static import serve

from website.sitemaps import SITEMAPS
from website.views import robots_txt

urlpatterns = [
    path('robots.txt', robots_txt, name='robots'),
    path(
        'sitemap.xml',
        sitemap,
        {'sitemaps': SITEMAPS},
        name='sitemap',
    ),
    path('admin/', admin.site.urls),
    path('panel/', include('panel.urls')),
    path('summernote/', include('django_summernote.urls')),
    path('api/bookings/', include('bookings.urls')),
    # Same-origin Font Awesome files (avoids R2 CORS blocking @font-face)
    re_path(
        r'^webfonts/(?P<path>.*)$',
        serve,
        {'document_root': settings.BASE_DIR / 'static' / 'webfonts'},
    ),
    path('', include('website.urls')),
]

handler404 = 'website.views.page_not_found'

if settings.DEBUG:
    urlpatterns += static('/static/', document_root=settings.BASE_DIR / 'static')
    if not getattr(settings, 'USE_R2_MEDIA', False):
        urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
