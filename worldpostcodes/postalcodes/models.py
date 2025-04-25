from django.contrib.gis.db import models
# Create your models here.


class RawPostalCode(models.Model):
    country = models.CharField(max_length=255, null=True, blank=True)
    country_code = models.CharField(max_length=255,null=True,blank=True)
    postal_code = models.CharField(max_length=255,null=True,blank=True)
    place_name = models.CharField(max_length=255,null=True,blank=True)
    admin_name1 = models.CharField(max_length=255,null=True,blank=True)
    admin_code1 = models.CharField(max_length=255,null=True,blank=True)
    admin_name2 = models.CharField(max_length=255,null=True,blank=True)
    admin_code2 = models.CharField(max_length=255,null=True,blank=True)
    admin_name3 = models.CharField(max_length=255,null=True,blank=True)
    admin_code3 = models.CharField(max_length=255,null=True,blank=True)
    latitude = models.FloatField()
    longitude = models.FloatField()
    accuracy = models.FloatField(null=True,blank=True)
    point = models.GeometryField(srid=4326)
    
    class Meta:
        indexes = [
            models.Index(fields=['country_code']),
        ]
