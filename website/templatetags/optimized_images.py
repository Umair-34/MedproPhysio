from django import template
from django.templatetags.static import static

from website.image_optimization import webp_exists_for_static, webp_exists_for_url, webp_url_for_url

register = template.Library()


def _resolve_urls(src: str):
    if src.startswith(('http://', 'https://', '/media/', '/static/')):
        original_url = src
        webp_url = webp_url_for_url(src)
        has_webp = webp_exists_for_url(src) if webp_url else False
        return original_url, webp_url if has_webp else None

    static_path = src.lstrip('/')
    if static_path.startswith('static/'):
        static_path = static_path[len('static/'):]

    original_url = static(static_path)
    webp_path = static_path.rsplit('.', 1)[0] + '.webp'
    has_webp = webp_exists_for_static(static_path)
    return original_url, static(webp_path) if has_webp else None


@register.inclusion_tag('includes/optimized_img.html')
def optimized_img(
    src,
    alt='',
    loading='lazy',
    width='',
    height='',
    css_class='',
    fetchpriority='',
):
    original_url, webp_url = _resolve_urls(src)
    return {
        'original_url': original_url,
        'webp_url': webp_url,
        'alt': alt,
        'loading': loading,
        'width': width,
        'height': height,
        'css_class': css_class,
        'fetchpriority': fetchpriority,
    }


@register.simple_tag
def optimized_static(src):
    """Return WebP static URL when available, otherwise the original static URL."""
    _original, webp_url = _resolve_urls(src)
    return webp_url or _original
