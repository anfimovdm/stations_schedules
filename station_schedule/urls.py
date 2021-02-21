from django.urls import path

from .views import (
    find_stations_and_create_entries,
    find_schedule_by_station_code,
)

app_name = 'station_schedule'
urlpatterns = [
    path(
        'find_stations_and_create_entries/',
        find_stations_and_create_entries,
        name='find_stations_and_create_entries',
    ),
    path('find_schedule_by_station_id/', find_schedule_by_station_code),
]
