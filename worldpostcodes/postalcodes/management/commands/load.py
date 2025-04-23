import os
import csv
import json
from django.conf import settings
from django.core.management.base import BaseCommand
from postalcodes.models import RawPostalCode
from django.contrib.gis.geos import GEOSGeometry,Point

class Command(BaseCommand):
    help = "insert data from allCountries.txt"

    def handle(self, *args, **options):
        objects_to_create = []
        data = []

        file_path = os.path.join(settings.BASE_DIR, 'allCountries.txt')
        with open(file_path, 'r', encoding='utf-8') as file:
            reader = csv.reader(file, delimiter='\t')
            for row in reader:
                latitude = float(row[9])
                longitude = float(row[10])
                if row[11] == '':
                    accuracy = 0
                else:
                    accuracy = row[11]

                entry = {
                    "country_code": row[0],
                    "postal_code": row[1],
                    "place_name": row[2],
                    "admin_name1": row[3],
                    "admin_code1": row[4],
                    "admin_name2": row[5],
                    "admin_code2": row[6],
                    "admin_name3": row[7],
                    "admin_code3": row[8],
                    "latitude": latitude,
                    "longitude": longitude,
                    "accuracy": accuracy
                }

                # Προαιρετικά GeoDjango point
                obj = RawPostalCode(
                    country_code=entry['country_code'],
                    postal_code=entry['postal_code'],
                    place_name=entry['place_name'],
                    admin_name1=entry['admin_name1'],
                    admin_code1=entry['admin_code1'],
                    admin_name2=entry['admin_name2'],
                    admin_code2=entry['admin_code2'],
                    admin_name3=entry['admin_name3'],
                    admin_code3=entry['admin_code3'],
                    latitude=entry['latitude'],
                    longitude=entry['longitude'],
                    accuracy=entry['accuracy'],
                    point=GEOSGeometry(Point(longitude, latitude))  # GeoDjango field
                )

                objects_to_create.append(obj)
                print(entry)
                data.append(entry)

        # Μαζική εισαγωγή
        RawPostalCode.objects.bulk_create(objects_to_create, batch_size=1000)

        # Εξαγωγή JSON
        json_path = os.path.join(settings.BASE_DIR, 'all.json')
        with open(json_path, 'w', encoding='utf-8') as json_file:
            json.dump(data, json_file, ensure_ascii=False, indent=2)

        self.stdout.write(self.style.SUCCESS(f'Εισάχθηκαν {len(objects_to_create)} εγγραφές.'))
