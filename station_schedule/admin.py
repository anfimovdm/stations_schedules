from django.contrib import admin

from .models import (
    Stations,
)
from .views import (
    find_schedule_by_station_code,
)


def find_schedule_by_station_code_and_update_entry(modeladmin, request, queryset):
    find_schedule_by_station_code(request, queryset)


class StationsAdmin(admin.ModelAdmin):
    actions = [find_schedule_by_station_code_and_update_entry]


admin.site.register(Stations, StationsAdmin)
