import requests
import json

from django.conf import settings
from django.db import transaction
from django.shortcuts import HttpResponseRedirect

from .models import Stations


def find_stations_and_create_entries(request):
    url = 'https://api.rasp.yandex.net/v3.0/nearest_stations'
    url_params = dict(
        apikey=settings.API_KEY,
        lat=48.7194,
        lng=44.5018,
        distance=50,
    )
    response = requests.get(
        url,
        params=url_params,
    )
    if response.status_code == 200:
        data = json.loads(response.text)
        stations = data.get('stations', {})
        if stations:
            exist_stations = tuple(Stations.objects.values_list(
                'code',
                flat=True,
            ).all())
            for station in stations:
                with transaction.atomic():
                    if station['code'] not in exist_stations:
                        Stations.objects.create(
                            code=station.get('code', ''),
                            type=station.get('type', ''),
                            station_type=station.get('station_type', ''),
                            station_type_name=station.get('station_type_name', ''),
                            title=station.get('title', ''),
                            transport_type=station.get('transport_type', ''),
                        )
    return HttpResponseRedirect('/admin/')


def find_schedule_by_station_code(request, queryset=None):
    url = 'https://api.rasp.yandex.net/v3.0/schedule'
    station_code = queryset.values_list(
        'code',
        flat=True,
    ).first()
    url_params = dict(
        apikey=settings.API_KEY,
        station=station_code,
    )
    response = requests.get(
        url,
        params=url_params,
    )
    if response.status_code == 200:
        result = []
        data = json.loads(response.text)
        schedules = data.get('schedule', {})
        if schedules:
            for schedule in schedules:
                thread = schedule.get('thread', '')
                title = thread.get('title', '') if thread else ''
                arrival = schedule.get('arrival', '')
                departure = schedule.get('departure', '')
                entry = f"{title} {arrival} {departure}<br>"
                result.append(entry)

            Stations.objects.filter(
                code=station_code,
            ).update(
                schedule=''.join(result),
            )

    return HttpResponseRedirect('')
