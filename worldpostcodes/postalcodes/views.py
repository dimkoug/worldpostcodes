from django.shortcuts import render
from django.views.generic import TemplateView
from django.core.cache import cache
# Create your views here.
from rest_framework import viewsets
from django.http import JsonResponse
from rest_framework.pagination import PageNumberPagination
from .models import RawPostalCode
from .serializers import PostalCodeGeoSerializer


class IndexView(TemplateView):
    template_name = "postalcodes/index.html"



class PostalCodePagination(PageNumberPagination):
    page_size = 10  # Adjust based on your performance tests

class PostalCodeGeoViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = PostalCodeGeoSerializer
    pagination_class = PostalCodePagination

    def get_queryset(self):
        query_params = self.request.query_params
        # Generate a sorted key string from query params
        sorted_items = sorted(query_params.items())
        key = 'postal_queryset_' + '_'.join(f'{k}-{v}' for k, v in sorted_items)
        print(f"Cache key: {key}")
        qs = cache.get(key)
        if not qs:
            print(f"{key} not exists")
            # qs = RawGeoName.objects.exclude(point__isnull=True)
            country = self.request.query_params.get('country_code')
            if country:
                qs = RawPostalCode.objects.filter(country_code=country)
            cache.set(key, qs, 86400)
        return qs
    


def country_list(request):
    countries = cache.get('postal_countries')
    if not countries:
        countries = (
            RawPostalCode.objects
            .exclude(country_code__isnull=True)
            .values_list('country_code', flat=True)
            .distinct()
            .order_by('country_code')
        )
        cache.set('postal_countries', countries, 86400)
    results = [{"id": code, "text": code} for code in countries]
    return JsonResponse({"results": results})