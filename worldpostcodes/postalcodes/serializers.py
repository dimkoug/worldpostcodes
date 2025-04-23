from rest_framework_gis.serializers import GeoFeatureModelSerializer
from .models import RawPostalCode

class PostalCodeGeoSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = RawPostalCode
        geo_field = "point"
        fields = ('postal_code', 'place_name')