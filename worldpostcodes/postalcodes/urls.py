from django.urls import path,include
from rest_framework.routers import DefaultRouter
from postalcodes.views import IndexView,PostalCodeGeoViewSet, country_list


app_name = 'postalcodes'

router = DefaultRouter()
router.register(r'postalcodes', PostalCodeGeoViewSet, basename='postalcode')


urlpatterns = [
    path('',IndexView.as_view(),name='index'),
    path('api/', include(router.urls)),
    path('api/countries/', country_list, name='country-list'),
]


