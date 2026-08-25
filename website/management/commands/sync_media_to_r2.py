"""Upload local media/ files to the configured default storage (Cloudflare R2)."""

from pathlib import Path

from django.conf import settings
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = 'Upload files from MEDIA_ROOT to default storage (one-time migration to R2).'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='List files that would be uploaded without uploading.',
        )
        parser.add_argument(
            '--force',
            action='store_true',
            help='Re-upload even when the key already exists on storage.',
        )

    def handle(self, *args, **options):
        if not getattr(settings, 'USE_R2_MEDIA', False):
            raise CommandError('USE_R2_MEDIA is not enabled. Nothing to sync.')

        media_root = Path(settings.MEDIA_ROOT)
        if not media_root.is_dir():
            self.stdout.write('No local media directory found.')
            return

        uploaded = 0
        skipped = 0

        for path in sorted(media_root.rglob('*')):
            if not path.is_file():
                continue

            name = path.relative_to(media_root).as_posix()
            exists = default_storage.exists(name)
            if exists and not options['force']:
                skipped += 1
                continue

            if options['dry_run']:
                self.stdout.write(f'Would upload: {name}')
                uploaded += 1
                continue

            if exists and options['force']:
                default_storage.delete(name)

            with path.open('rb') as handle:
                default_storage.save(name, ContentFile(handle.read()))
            uploaded += 1
            if uploaded % 25 == 0:
                self.stdout.write(f'Uploaded {uploaded} files…')

        self.stdout.write(
            self.style.SUCCESS(
                f'Done. Uploaded {uploaded}, skipped {skipped} (already on storage).'
            )
        )
