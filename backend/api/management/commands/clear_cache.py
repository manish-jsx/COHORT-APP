from django.core.management.base import BaseCommand
from django.core.cache import caches

class Command(BaseCommand):
    help = "Clears the Django cache"

    def add_arguments(self, parser):
        parser.add_argument('cache_name', nargs='?', type=str, default='default', help='The name of the cache to clear (defaults to "default")')

    def handle(self, *args, **options):
        cache_name = options['cache_name']
        try:
            cache = caches[cache_name]
            cache.clear()
            self.stdout.write(self.style.SUCCESS(f'Cleared cache "{cache_name}"'))
        except KeyError:
            self.stdout.write(self.style.ERROR(f'Cache "{cache_name}" not found'))
