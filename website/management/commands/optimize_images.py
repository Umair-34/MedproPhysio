from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand

from website.image_optimization import optimize_directory


class Command(BaseCommand):
    help = 'Convert JPG/PNG images to optimized WebP versions for faster page loads.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--force',
            action='store_true',
            help='Rebuild WebP files even when they are newer than the source image.',
        )
        parser.add_argument(
            '--static-only',
            action='store_true',
            help='Only optimize files in static/images.',
        )
        parser.add_argument(
            '--media-only',
            action='store_true',
            help='Only optimize uploaded media files.',
        )

    def handle(self, *args, **options):
        force = options['force']
        static_only = options['static_only']
        media_only = options['media_only']

        targets = []
        if not media_only:
            targets.append(('static/images', Path(settings.BASE_DIR) / 'static' / 'images'))
            targets.append(
                ('page assets', Path(settings.BASE_DIR) / 'website' / 'assets' / 'page_images')
            )
        if not static_only:
            targets.append(('media', Path(settings.MEDIA_ROOT)))

        total_processed = 0
        total_saved = 0
        total_original = 0
        total_webp = 0

        for label, directory in targets:
            stats = optimize_directory(directory, force=force)
            total_processed += stats['processed']
            total_saved += stats['saved_bytes']
            total_original += stats['original_bytes']
            total_webp += stats['webp_bytes']
            saved_mb = stats['saved_bytes'] / (1024 * 1024)
            self.stdout.write(
                f'{label}: {stats["processed"]} WebP files '
                f'({saved_mb:.1f} MB smaller than originals where converted)'
            )

        if total_original:
            reduction = (1 - (total_webp / total_original)) * 100
            self.stdout.write(
                self.style.SUCCESS(
                    f'Done. {total_processed} images optimized. '
                    f'Estimated transfer reduction: {reduction:.0f}% '
                    f'({total_saved / (1024 * 1024):.1f} MB saved vs originals).'
                )
            )
        else:
            self.stdout.write(self.style.WARNING('No raster images found to optimize.'))
