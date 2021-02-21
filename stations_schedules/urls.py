from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('station_schedule/', include('station_schedule.urls')),
]
