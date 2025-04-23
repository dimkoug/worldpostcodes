from django.contrib.gis.db import models
# Create your models here.

class Country(models.Model):
    name = models.CharField(max_length=255,null=True,blank=True)
    alpha2 = models.CharField(max_length=255,null=True,blank=True)
    alpha3 = models.CharField(max_length=255,null=True,blank=True)
    country_code = models.CharField(max_length=255,null=True,blank=True)
    region = models.CharField(max_length=255,null=True,blank=True)
    sub_region = models.CharField(max_length=255,null=True,blank=True)
    intermediate_region = models.CharField(max_length=255,null=True,blank=True)


class RawGeoName(models.Model):
    geonameid = models.BigIntegerField(null=True,blank=True)
    name = models.CharField(max_length=255,null=True,blank=True)
    asciiname = models.CharField(max_length=255,null=True,blank=True)
    alternatenames = models.CharField(max_length=10000,null=True,blank=True)
    latitude = models.FloatField()
    longitude = models.FloatField()
    feature_class = models.CharField(max_length=255,null=True,blank=True)
    feature_code = models.CharField(max_length=255,null=True,blank=True)
    country_code = models.CharField(max_length=255,null=True,blank=True)
    cc2 = models.CharField(max_length=255,null=True,blank=True)
    admin1_code = models.CharField(max_length=255,null=True,blank=True)
    admin2_code = models.CharField(max_length=255,null=True,blank=True)
    admin3_code = models.CharField(max_length=255,null=True,blank=True)
    admin4_code = models.CharField(max_length=255,null=True,blank=True)
    population = models.BigIntegerField(null=True,blank=True)
    elevation = models.BigIntegerField(null=True,blank=True)
    dem = models.BigIntegerField(null=True,blank=True)
    point = models.GeometryField(srid=4326)
    
    class Meta:
        indexes = [
            models.Index(fields=['country_code']),
        ]

