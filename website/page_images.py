from pathlib import Path

from django.conf import settings
from django.core.files import File

ASSETS_DIR = Path(settings.BASE_DIR) / 'website' / 'assets' / 'page_images'
FALLBACK_IMAGE = 'content-physiotherapy-clinic.jpg'

ACUPUNCTURE_NEEDLING_IMAGE = 'content-acupuncture-wellness.jpg'

# Explicit slug to image map so every page gets a title related image.
SLUG_IMAGE_MAP = {
    # Focus areas
    'sports-recovery': 'content-sports-physio.jpg',
    'workplace-acc-injuries': 'content-workplace-injury.jpg',
    'motor-vehicle-accident': 'content-workplace-injury.jpg',
    'post-surgery-rehab': 'content-post-surgery-rehab.jpg',
    'balance-vestibular': 'content-balance-vestibular.jpg',
    'pregnancy-postnatal': 'content-pregnancy-physio.jpg',
    'chronic-pain': 'content-chronic-pain.jpg',
    'pelvic-health': 'content-pregnancy-physio.jpg',
    'concussion-recovery': 'content-concussion-management.jpg',
    'acupuncture-wellness': ACUPUNCTURE_NEEDLING_IMAGE,

    # Conditions
    'back-sciatica-pain': 'content-physiotherapy-clinic.jpg',
    'shoulder-pain': 'content-physiotherapy-clinic.jpg',
    'foot-ankle-pain': 'content-physiotherapy-clinic.jpg',
    'arthritis': 'content-chronic-pain.jpg',
    'fibromyalgia': 'content-chronic-pain.jpg',
    'acc-injuries': 'content-workplace-injury.jpg',
    'poor-posture': 'content-chiropractic-care.jpg',
    'pre-surgery-prep': 'content-post-surgery-rehab.jpg',
    'sports-injuries': 'content-sports-physio.jpg',
    'tmj-dysfunction': 'content-chiropractic-care.jpg',
    'vestibular-issues': 'content-balance-vestibular.jpg',
    'neck-pain': 'content-chiropractic-care.jpg',
    'hip-knee-pain': 'content-physiotherapy-clinic.jpg',
    'elbow-wrist-hand-pain': 'content-physiotherapy-clinic.jpg',
    'balance-gait': 'content-balance-vestibular.jpg',
    'dizziness-vertigo': 'content-balance-vestibular.jpg',
    'headaches-migraines': 'content-chronic-pain.jpg',
    'pelvic-pain': 'content-physiotherapy-clinic.jpg',
    'prenatal-postnatal-pain': 'content-pregnancy-physio.jpg',
    'post-surgical-rehab': 'content-post-surgery-rehab.jpg',
    'work-injuries': 'content-workplace-injury.jpg',
    'pelvic-floor-therapy': 'content-pregnancy-physio.jpg',
    'concussions': 'content-concussion-management.jpg',

    # Treatments
    'physiotherapy': 'content-physiotherapy-clinic.jpg',
    'massage-therapy': 'content-massage-therapy.jpg',
    'manual-therapy': 'content-manual-therapy.jpg',
    'exercise-rehab': 'content-kinesiology-exercise.jpg',
    'kinesiology': 'content-kinesiology-exercise.jpg',
    'dry-needling': ACUPUNCTURE_NEEDLING_IMAGE,
    'balance-fall-prevention': 'content-balance-vestibular.jpg',
    'joint-mobilisation': 'content-manual-therapy.jpg',
    'sports-performance': 'content-sports-physio.jpg',
    'chiropractic': 'content-chiropractic-care.jpg',
    'acupuncture': ACUPUNCTURE_NEEDLING_IMAGE,
    'myofascial-release': 'content-massage-therapy.jpg',
    'ultrasound-therapy': 'content-ultrasound-therapy.jpg',
    'kinesio-taping': 'content-kinesio-taping.jpg',
    'mckenzie-method': 'content-manual-therapy.jpg',
    'ergonomic-training': 'content-workplace-injury.jpg',
    'vestibular-therapy': 'content-balance-vestibular.jpg',
    'postural-restoration': 'content-chiropractic-care.jpg',
    'electrical-stimulation': 'content-electrical-stimulation.jpg',
    'concussion-management': 'content-concussion-management.jpg',
}

# Fallback matching from slug or page title text.
TITLE_KEYWORD_RULES = (
    (('dry needling', 'acupuncture', 'needling'), ACUPUNCTURE_NEEDLING_IMAGE),
    (('ultrasound',), 'content-ultrasound-therapy.jpg'),
    (('electrical', 'stimulation', 'tens'), 'content-electrical-stimulation.jpg'),
    (('kinesio taping', 'taping'), 'content-kinesio-taping.jpg'),
    (('manual therapy', 'manual', 'mobil', 'mckenzie'), 'content-manual-therapy.jpg'),
    (('massage', 'myofascial'), 'content-massage-therapy.jpg'),
    (('chiropractic', 'tmj', 'jaw', 'posture', 'postural', 'neck'), 'content-chiropractic-care.jpg'),
    (('kinesiology', 'exercise', 'sports performance', 'sports'), 'content-kinesiology-exercise.jpg'),
    (('sport', 'concussion'), 'content-concussion-management.jpg'),
    (('work', 'wcb', 'workplace', 'ergonomic', 'motor vehicle', 'mva', 'accident'), 'content-workplace-injury.jpg'),
    (('pregnan', 'postnatal', 'prenatal'), 'content-pregnancy-physio.jpg'),
    (('pelvic pain',), 'content-physiotherapy-clinic.jpg'),
    (('post surg', 'pre surg', 'surgical'), 'content-post-surgery-rehab.jpg'),
    (('balance', 'vestibular', 'dizziness', 'vertigo', 'gait', 'fall prevention'), 'content-balance-vestibular.jpg'),
    (('chronic', 'fibromyalgia', 'arthritis', 'headache', 'migraine'), 'content-chronic-pain.jpg'),
    (('physio',), 'content-physiotherapy-clinic.jpg'),
)


def _match_title_keywords(text):
    text_lower = text.lower()
    for keywords, filename in TITLE_KEYWORD_RULES:
        if any(keyword in text_lower for keyword in keywords):
            return filename
    return None


def resolve_image_filename(slug, section='', title=''):
    if slug in SLUG_IMAGE_MAP:
        return SLUG_IMAGE_MAP[slug]

    for text in (slug.replace('-', ' '), title):
        matched = _match_title_keywords(text)
        if matched:
            return matched

    if section == 'treatments':
        return 'content-physiotherapy-clinic.jpg'
    return FALLBACK_IMAGE


def assign_page_images(pages=None, force=False):
    """Upload bundled page images into each ContentPage image field."""
    from website.models import ContentPage

    if pages is None:
        queryset = ContentPage.objects.order_by('section', 'sort_order', 'id')
        pages = list(queryset if force else [page for page in queryset if not page.image])

    assigned = 0
    for page in pages:
        filename = resolve_image_filename(page.slug, page.section, page.title)
        source_path = ASSETS_DIR / filename
        if not source_path.exists():
            source_path = ASSETS_DIR / FALLBACK_IMAGE
        if not source_path.exists():
            continue

        if page.image:
            page.image.delete(save=False)

        with source_path.open('rb') as image_file:
            page.image.save(f'{page.slug}.jpg', File(image_file), save=False)

        page.image_alt = f'{page.title} at Medpro Physio Calgary'
        page.save(update_fields=['image', 'image_alt'])

        from website.image_optimization import convert_to_webp
        try:
            convert_to_webp(page.image.path)
        except NotImplementedError:
            convert_to_webp(source_path)

        assigned += 1

    return assigned


def assign_default_page_images(pages=None):
    """Backward compatible alias used by seed migrations."""
    return assign_page_images(pages=pages, force=not pages)
