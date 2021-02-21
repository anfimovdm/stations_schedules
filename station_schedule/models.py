from django.db import models

from ckeditor.fields import RichTextField


class Stations(models.Model):
    code = models.CharField(max_length=200, null=True, blank=True)
    type = models.CharField(max_length=50, null=True, blank=True)
    station_type = models.CharField(max_length=100, null=True, blank=True)
    station_type_name = models.CharField(max_length=200, null=True, blank=True)
    title = models.CharField(max_length=200, null=True, blank=True)
    transport_type = models.CharField(max_length=50, null=True, blank=True)
    schedule = RichTextField(null=True, blank=True)

    class Meta:
        db_table = 'stations'
        verbose_name = verbose_name_plural = 'Станции'
