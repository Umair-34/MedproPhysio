"""Image optimization helpers: WebP conversion and responsive sizing."""

from __future__ import annotations

from pathlib import Path

from django.conf import settings
from PIL import Image

RASTER_EXTENSIONS = {'.jpg', '.jpeg', '.png'}
WEBP_QUALITY = 82
DEFAULT_MAX_WIDTH = 1400
HERO_MAX_WIDTH = 1920
THUMBNAIL_MAX_WIDTH = 800

HERO_BASENAMES = {
    'hero-bg',
    'hero-bg-2',
    'how-work-feature',
    'page-header',
    'cta-box-bg',
}

THUMBNAIL_BASENAMES = {
    'team-1',
    'team-2',
    'team-3',
    'team-4',
    'author-',
    'post-',
    'about-us-img',
}


def is_raster_path(path: Path | str) -> bool:
    return Path(path).suffix.lower() in RASTER_EXTENSIONS


def webp_path_for(path: Path | str) -> Path:
    return Path(path).with_suffix('.webp')


def webp_url_for_url(url: str | None) -> str | None:
    if not url:
        return None
    lower = url.lower()
    for ext in ('.jpg', '.jpeg', '.png'):
        if lower.endswith(ext):
            return f'{url[:-len(ext)]}.webp'
    return None


def webp_url_for_field(field_file) -> str | None:
    """Return a sibling WebP URL for an ImageField/FileField, including R2/S3."""
    if not field_file:
        return None
    webp_url = webp_url_for_url(field_file.url)
    if not webp_url:
        return None
    try:
        webp_file = webp_path_for(field_file.path)
    except NotImplementedError:
        return webp_url
    if webp_file.exists():
        return webp_url
    return None


def _max_width_for(path: Path) -> int:
    stem = path.stem.lower()
    if any(hero in stem for hero in HERO_BASENAMES):
        return HERO_MAX_WIDTH
    if any(thumb in stem for thumb in THUMBNAIL_BASENAMES):
        return THUMBNAIL_MAX_WIDTH
    return DEFAULT_MAX_WIDTH


def _prepare_image(image: Image.Image, max_width: int) -> Image.Image:
    if image.mode in ('RGBA', 'LA'):
        background = Image.new('RGBA', image.size, (255, 255, 255, 255))
        background.paste(image, mask=image.split()[-1])
        image = background.convert('RGB')
    elif image.mode != 'RGB':
        image = image.convert('RGB')

    if image.width > max_width:
        ratio = max_width / image.width
        new_height = max(1, int(image.height * ratio))
        image = image.resize((max_width, new_height), Image.Resampling.LANCZOS)
    return image


def convert_to_webp(
    source_path: Path,
    *,
    quality: int = WEBP_QUALITY,
    max_width: int | None = None,
    force: bool = False,
) -> tuple[Path | None, int, int]:
    """
    Create a WebP version beside the source image.
    Returns (webp_path, original_bytes, webp_bytes).
    """
    source_path = Path(source_path)
    if not source_path.exists() or not is_raster_path(source_path):
        return None, 0, 0

    destination = webp_path_for(source_path)
    original_bytes = source_path.stat().st_size

    if destination.exists() and not force:
        if destination.stat().st_mtime >= source_path.stat().st_mtime:
            return destination, original_bytes, destination.stat().st_size

    max_width = max_width or _max_width_for(source_path)

    with Image.open(source_path) as image:
        prepared = _prepare_image(image, max_width)
        prepared.save(
            destination,
            format='WEBP',
            quality=quality,
            method=6,
        )

    return destination, original_bytes, destination.stat().st_size


def optimize_directory(
    directory: Path,
    *,
    force: bool = False,
    max_width: int | None = None,
) -> dict:
    stats = {
        'processed': 0,
        'skipped': 0,
        'saved_bytes': 0,
        'original_bytes': 0,
        'webp_bytes': 0,
    }

    if not directory.exists():
        return stats

    for source_path in sorted(directory.rglob('*')):
        if not source_path.is_file() or not is_raster_path(source_path):
            continue

        webp_path, original_bytes, webp_bytes = convert_to_webp(
            source_path,
            force=force,
            max_width=max_width,
        )
        if not webp_path:
            stats['skipped'] += 1
            continue

        stats['processed'] += 1
        stats['original_bytes'] += original_bytes
        stats['webp_bytes'] += webp_bytes
        stats['saved_bytes'] += max(0, original_bytes - webp_bytes)

    return stats


def static_file_path(static_path: str) -> Path | None:
    relative = static_path.lstrip('/')
    if relative.startswith('static/'):
        relative = relative[len('static/'):]

    for root in (Path(settings.BASE_DIR) / 'static',):
        candidate = root / relative
        if candidate.exists():
            return candidate
    return None


def webp_exists_for_static(static_path: str) -> bool:
    source = static_file_path(static_path)
    if not source:
        return False
    return webp_path_for(source).exists()


def webp_exists_for_url(url: str) -> bool:
    webp_url = webp_url_for_url(url)
    if not webp_url:
        return False

    if url.startswith(settings.MEDIA_URL):
        relative = url[len(settings.MEDIA_URL):].lstrip('/')
        webp_relative = webp_path_for(relative).as_posix()

        # Remote media (R2/S3): confirm the sibling WebP object exists in storage.
        if settings.MEDIA_URL.startswith(('http://', 'https://')):
            from django.core.files.storage import default_storage

            try:
                return default_storage.exists(webp_relative)
            except Exception:
                return False

        candidate = Path(settings.MEDIA_ROOT) / relative
        return webp_path_for(candidate).exists()

    if url.startswith('/static/') or 'static/' in url:
        static_path = url.split('/static/', 1)[-1]
        return webp_exists_for_static(static_path)

    return False
