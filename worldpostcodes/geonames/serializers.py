from rest_framework_gis.serializers import GeoFeatureModelSerializer
from .models import RawGeoName

class RawGeoNameGeoSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = RawGeoName
        geo_field = "point"
        fields = ('name', 'country_code')