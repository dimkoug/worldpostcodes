from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from django.http import JsonResponse
from rest_framework.pagination import PageNumberPagination
from .models import RawGeoName
from .serializers import RawGeoNameGeoSerializer

class RawGeoNamePagination(PageNumberPagination):
    page_size = 10  # Adjust based on your performance tests

class RawGeoNameGeoViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = RawGeoNameGeoSerializer
    pagination_class = RawGeoNamePagination

    def get_queryset(self):
        qs = RawGeoName.objects.exclude(point__isnull=True)
        country = self.request.query_params.get('country_code')
        if country:
            qs = qs.filter(country_code=country)
        return qs
    


def geo_country_list(request):
    countries = (
        RawGeoName.objects
        .exclude(country_code__isnull=True)
        .values_list('country_code', flat=True)
        .distinct()
        .order_by('country_code')
    )
    results = [{"id": code, "text": code} for code in countries]
    return JsonResponse({"results": results})