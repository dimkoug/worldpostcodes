import os
import csv
import json
from django.conf import settings
from django.core.management.base import BaseCommand
from geonames.models import RawGeoName
from django.contrib.gis.geos import GEOSGeometry,Point

class Command(BaseCommand):
    help = "indert data from allCountries.txt"

    def handle(self, *args, **options):
        objects_to_create = []
        data = []

        file_path = os.path.join(settings.BASE_DIR, 'allCountries.txt')
        with open(file_path, 'r', encoding='utf-8') as file:
            reader = csv.reader(file, delimiter='\t')
            for row in reader:
                latitude = float(row[4])
                longitude = float(row[5])


                entry = {
                    "geonameid": row[0],
                    "name": row[1],
                    "asciiname": row[2],
                    "alternatenames": row[3],
                    "latitude": latitude,
                    "longitude": longitude,
                    "feature_class": row[6],
                    "feature_code": row[7],
                    "country_code": row[8],
                    "cc2": row[9],
                    "admin1_code": row[10],
                    "admin2_code": row[11],
                    "admin3_code": row[12],
                    "admin4_code": row[13],
                    "population": int(row[14]) if row[14].isdigit() else 0,
                    "elevation": int(row[15]) if row[15].isdigit() else None,
                    "dem": row[16],
                    "point":GEOSGeometry(f'POINT({longitude} {latitude})')
                }
                if len(objects_to_create) == 10000:
                    RawGeoName.objects.bulk_create(objects_to_create, batch_size=1000)
                    objects_to_create = []

                # Προαιρετικά GeoDjango point
                obj = RawGeoName(**entry)
                objects_to_create.append(obj)
                print(entry)
                data.append(entry)

        # Μαζική εισαγωγή
        RawGeoName.objects.bulk_create(objects_to_create, batch_size=1000)

        # Εξαγωγή JSON
        json_path = os.path.join(settings.BASE_DIR, 'countries.json')
        with open(json_path, 'w', encoding='utf-8') as json_file:
            json.dump(data, json_file, ensure_ascii=False, indent=2)

        self.stdout.write(self.style.SUCCESS(f'Εισάχθηκαν {len(objects_to_create)} εγγραφές.'))
