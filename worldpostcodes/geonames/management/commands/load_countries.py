import csv
import os
from django.conf import settings
from django.core.management.base import BaseCommand
from geonames.models import Country  # change to your app name

class Command(BaseCommand):
    help = 'Import countries from CSV'

    def handle(self, *args, **kwargs):
        with open(os.path.join(settings.BASE_DIR,'all.csv'), newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                Country.objects.update_or_create(
                    alpha2=row['alpha-2'],
                    defaults={
                        'name': row['name'],
                        'alpha3': row['alpha-3'],
                        'country_code': row['country-code'],
                        'region': row['region'],
                        'sub_region': row['sub-region'],
                        'intermediate_region': row['intermediate-region'],
                    }
                )
        self.stdout.write(self.style.SUCCESS('Countries imported successfully.'))