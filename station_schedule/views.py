import requests
import json

from django.conf import settings
from django.db import transaction
from django.shortcuts import HttpResponseRedirect, HttpResponse

from .models import Stations


# Координаты Волгограда
LATITUDE_VLG = 48.7194
LONGITUDE_VLG = 44.5018
# Макс. дистанция в км
MAX_DISTANCE = 50


def find_stations_and_create_entries(request):
    html = '<html><body>{}</body></html>'
    url = 'https://api.rasp.yandex.net/v3.0/nearest_stations'
    url_params = dict(
        apikey=settings.API_KEY,
        lat=LATITUDE_VLG,
        lng=LONGITUDE_VLG,
        distance=MAX_DISTANCE,
    )
    response = requests.get(
        url,
        params=url_params,
    )
    if response.status_code == 200:
        data = json.loads(response.text)
        stations = data.get('stations', {})
        if stations:
            for station in stations:
                code = station.get('code', '')
                default_params = dict(
                    type=station.get('type', ''),
                    station_type=station.get('station_type', ''),
                    station_type_name=station.get('station_type_name', ''),
                    title=station.get('title', ''),
                    transport_type=station.get('transport_type', ''),
                    schedule='',
                )
                with transaction.atomic():
                    try:
                        Stations.objects.update_or_create(
                            code=code,
                            defaults=default_params,
                        )
                    except Stations.MultipleObjectsReturned:
                        return HttpResponse(
                            html.format(
                                f'Найдено несколько станций с кодом {code}. Импорт прерван.',
                            ),
                        )
    return HttpResponse(
        html.format(
            'Импорт успешно завершен',
        ),
    )


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
                entry = f"<b>Маршрут:</b> {title}, <b>прибытие:</b> {arrival}, <b>убытие:</b> {departure}.<br>"
                result.append(entry)
            with transaction.atomic():
                Stations.objects.filter(
                    code=station_code,
                ).update(
                    schedule=''.join(result),
                )
    return HttpResponseRedirect('')
