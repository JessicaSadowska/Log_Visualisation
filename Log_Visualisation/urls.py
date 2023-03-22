from django.contrib import admin
from django.urls import path

from Log_Visualisation_App.views import Home

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', Home.as_view(), name='Home'),
]
