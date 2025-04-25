import psutil
import sys
from django.db import models
from django.core.management.base import BaseCommand
from geonames.models import Country, RawGeoName
from postalcodes.models import RawPostalCode

def estimate_model_instance_size(model_class):
    """
    Estimate the memory size (in bytes) of a single instance of a Django model.
    """
    field_size_estimates = {
        models.CharField: 100,    # assume average 100 bytes
        models.TextField: 500,    # longer text
        models.IntegerField: 4,   # 4 bytes
        models.BigIntegerField: 8,
        models.BooleanField: 1,
        models.DateTimeField: 8,
        models.DateField: 4,
        models.FloatField: 8,
        models.DecimalField: 16,
        models.ForeignKey: 4,     # usually an integer id
        models.OneToOneField: 4,
    }

    total_size = 0
    for field in model_class._meta.get_fields():
        if not hasattr(field, 'attname'):  # skip reverse relations
            continue
        for field_type, size in field_size_estimates.items():
            if isinstance(field, field_type):
                total_size += size
                break
        else:
            # default guess for unknown fields
            total_size += 50

    return total_size

def calculate_dynamic_batch_size(model_class, memory_fraction=0.05, min_batch=500, max_batch=10000):
    """
    Dynamically calculate batch size based on available memory and estimated model size.
    """
    total_memory = psutil.virtual_memory().total
    available_memory = total_memory * memory_fraction

    instance_size = estimate_model_instance_size(model_class)
    batch_size = int(available_memory / instance_size)

    return max(min_batch, min(batch_size, max_batch))

class Command(BaseCommand):
    help = "map countries to postal codes"

    def handle(self, *args, **options):
        batch_size = calculate_dynamic_batch_size(RawPostalCode)
        self.stdout.write(f"Using batch size: {batch_size}")  # you can tune this based on your memory

        for country in Country.objects.all():
            qs = RawPostalCode.objects.filter(country_code=country.alpha2)
            total = qs.count()

            if total == 0:
                continue

            self.stdout.write(f'Updating {total} postal codes for country {country.name}...')

            for start in range(0, total, batch_size):
                batch = qs[start:start+batch_size]

                # Update the objects in memory
                for postal_code in batch:
                    postal_code.country = country.name

                RawPostalCode.objects.bulk_update(batch, fields=['country'])

        batch_size = calculate_dynamic_batch_size(RawGeoName)
        self.stdout.write(f"Using batch size: {batch_size}")
        for country in Country.objects.all():
            qs = RawGeoName.objects.filter(country_code=country.alpha2)
            total = qs.count()

            if total == 0:
                continue

            self.stdout.write(f'Updating {total} geonames for country {country.name}...')

            for start in range(0, total, batch_size):
                batch = qs[start:start+batch_size]

                # Update the objects in memory
                for geoname in batch:
                    geoname.country = country.name

                RawGeoName.objects.bulk_update(batch, fields=['country'])

        self.stdout.write(self.style.SUCCESS('Done'))
