from django.urls import path,include
from rest_framework.routers import DefaultRouter

from rest_framework.routers import DefaultRouter
from geonames.views import IndexView, RawGeoNameGeoViewSet, geo_country_list
router = DefaultRouter()
router.register(r'geonames', RawGeoNameGeoViewSet, basename='geoname')

app_name = 'geonames'


urlpatterns = [
    path('',IndexView.as_view(),name='index'),
    path('api/', include(router.urls)),
    path('api/countries/', geo_country_list, name='country-list'),
]
