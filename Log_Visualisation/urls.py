from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from Log_Visualisation import settings
from Log_Visualisation_App.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', Home.as_view(), name='Home'),
    path('uploaded-logs-with-object/<int:log_id>/', UploadedLogsWithObject.as_view(), name='UploadedLogsWithObject'),
    path('uploaded-logs-with-event-name/<int:log_id>/', UploadedLogsWithEventName.as_view(), name='UploadedLogsWithEventName')
]

