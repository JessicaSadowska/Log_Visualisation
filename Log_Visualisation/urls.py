from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from Log_Visualisation import settings
from Log_Visualisation_App.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', Home.as_view(), name='Home'),
    path('logs-with-event-name/<int:log_id>/', LogsWithEventName.as_view(), name='LogsWithEventName'),
    path('logs-with-activity/<int:log_id>/', LogsWithActivity.as_view(), name='LogsWithActivity'),
    path('logs-with-object/<int:log_id>/', LogsWithObject.as_view(), name='LogsWithObject'),
    path('logs-with-object-type/<int:log_id>/', LogsWithObjectType.as_view(), name='LogsWithObjectType'),
    path('draw/<int:log_id>/', Draw.as_view(), name='Draw')
]

