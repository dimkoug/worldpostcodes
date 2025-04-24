from django.shortcuts import render
from django.core.cache import cache
from django.views.generic import TemplateView
# Create your views here.
from rest_framework import viewsets
from django.http import JsonResponse
from rest_framework.pagination import PageNumberPagination
from .models import RawGeoName
from .serializers import RawGeoNameGeoSerializer


class IndexView(TemplateView):
    template_name = "geonames/index.html"



class RawGeoNamePagination(PageNumberPagination):
    page_size = 10  # Adjust based on your performance tests

class RawGeoNameGeoViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = RawGeoNameGeoSerializer
    pagination_class = RawGeoNamePagination

    def get_queryset(self):
        query_params = self.request.query_params
        # Generate a sorted key string from query params
        sorted_items = sorted(query_params.items())
        key = 'geo_queryset_' + '_'.join(f'{k}-{v}' for k, v in sorted_items)
        print(f"Cache key: {key}")
        qs = cache.get(key)
        if not qs:
            print(f"{key} not exists")
            # qs = RawGeoName.objects.exclude(point__isnull=True)
            country = self.request.query_params.get('country_code')
            if country:
                qs = RawGeoName.objects.filter(country_code=country)
            cache.set(key, qs, 86400)
        return qs
    


def geo_country_list(request):
    countries = cache.get('countries')
    if not countries:
        countries = (
            RawGeoName.objects
            .exclude(country_code__isnull=True)
            .values_list('country_code', flat=True)
            .distinct()
            .order_by('country_code')
        )
        cache.set('countries', countries, 86400)
    results = [{"id": code, "text": code} for code in countries]
    return JsonResponse({"results": results})