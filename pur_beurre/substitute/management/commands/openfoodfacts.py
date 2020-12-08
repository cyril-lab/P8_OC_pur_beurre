from django.core.management.base import BaseCommand, CommandError
from substitute.models import Category, Product
from substitute.services.application import Application


class Command(BaseCommand):
    help = 'Download data from openfoodfacts'

    def add_arguments(self, parser):
        # Positional arguments
        # parser.add_argument('poll_ids', nargs='+', type=int)

        # Named (optional) arguments
        parser.add_argument(
            '--delete',
            action='store_true',
            help='truncate database',
        )

    def handle(self, *args, **options):
        if options['delete']:
            try:
                Category.objects.all().delete()
                Product.objects.all().delete()
                self.stdout.write('Données supprimées')
            except:
                pass
        else:
            application = Application('Snack', 'Desserts')
            application.main()

