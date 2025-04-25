import psutil
import sys
from django.db import models
from django.core.management.base import BaseCommand
from django.core.cache import cache
from geonames.models import Country, RawGeoName
from postalcodes.models import RawPostalCode

class Command(BaseCommand):
    help = "Load cache for postal codes and geonames"

    def handle(self, *args, **options):
        for country in Country.objects.all():
            qs_1 = RawPostalCode.objects.filter(country_code=country.alpha2)
            if not qs_1.exists():
                self.stdout.write(self.style.ERROR(f"postal code country {country.alpha2} not exists"))
                continue
            cache.set(f'postal_queryset_{country.alpha2}', qs_1, 86400)
            self.stdout.write(self.style.SUCCESS(f"Country {country.alpha2} cached"))
            qs_2 = RawGeoName.objects.filter(country_code=country.alpha2)
            if not qs_2.exists():
                self.stdout.write(self.style.ERROR(f"geoname Country {country.alpha2} not exists"))
                continue
            cache.set(f'geoname_queryset_{country.alpha2}', qs_2, 86400)
            self.stdout.write(self.style.SUCCESS(f"geoname Country {country.alpha2} cached"))


        self.stdout.write(self.style.SUCCESS('Warm cache Done'))
