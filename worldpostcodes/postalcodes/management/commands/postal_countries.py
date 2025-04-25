from django.core.management.base import BaseCommand
from geonames.models import Country, RawGeoName
from postalcodes.models import RawPostalCode


class Command(BaseCommand):
    help = "map countries to postal codes"

    def handle(self, *args, **options):
        BATCH_SIZE = 1000  # you can tune this based on your memory

        for country in Country.objects.all():
            qs = RawPostalCode.objects.filter(country_code=country.alpha2)
            total = qs.count()

            if total == 0:
                continue

            self.stdout.write(f'Updating {total} postal codes for country {country.name}...')

            for start in range(0, total, BATCH_SIZE):
                batch = qs[start:start+BATCH_SIZE]

                # Update the objects in memory
                for postal_code in batch:
                    postal_code.country = country.name

                RawPostalCode.objects.bulk_update(batch, fields=['country'])

        for country in Country.objects.all():
            qs = RawGeoName.objects.filter(country_code=country.alpha2)
            total = qs.count()

            if total == 0:
                continue

            self.stdout.write(f'Updating {total} geonames for country {country.name}...')

            for start in range(0, total, BATCH_SIZE):
                batch = qs[start:start+BATCH_SIZE]

                # Update the objects in memory
                for geoname in batch:
                    geoname.country = country.name

                RawGeoName.objects.bulk_update(batch, fields=['country'])

        self.stdout.write(self.style.SUCCESS('Done'))
