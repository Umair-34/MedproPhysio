from django.core.management.base import BaseCommand

from website.page_images import assign_page_images


class Command(BaseCommand):
    help = 'Upload bundled AI page images to all content pages.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--force',
            action='store_true',
            help='Replace images even when a page already has one uploaded.',
        )

    def handle(self, *args, **options):
        assigned = assign_page_images(force=options['force'])
        self.stdout.write(self.style.SUCCESS(f'Uploaded images for {assigned} content page(s).'))
