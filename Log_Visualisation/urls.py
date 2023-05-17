from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from Log_Visualisation import settings
from Log_Visualisation_App.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', Home.as_view(), name='Home'),
    path('logs-with-event-name/<int:log_id>/<str:event_name>/', LogsWithEventName.as_view(), name='LogsWithEventName'),
    path('logs-with-activity/<int:log_id>/<str:activity>/', LogsWithActivity.as_view(), name='LogsWithActivity'),
    path('logs-with-object/<int:log_id>/<str:object_id>/', LogsWithObject.as_view(), name='LogsWithObject'),
    path('logs-with-object-type/<int:log_id>/<str:object_type>/', LogsWithObjectType.as_view(), name='LogsWithObjectType'),
    path('draw-table/<int:log_id>/', DrawTable.as_view(), name='DrawTable'),
    path('draw-dependencies-of-objects/<int:log_id>/<int:object_id>/', DrawDependenciesOfObjects.as_view(), name='DrawDependenciesOfObjects'),
    path('draw-another-dependencies/<int:log_id>/<str:event_name>/', DrawAnotherDependencies.as_view(), name='DrawAnotherDependencies'),
    path('statistics/<int:log_id>/', Statistics.as_view(), name='Statistics'),
    path('graphs/<int:log_id>/', Graphs.as_view(), name='Graphs'),
    path('graphs-uploaded/<int:log_id>/<int:object_id>/', GraphsUploaded.as_view(), name='GraphsUploaded'),
    path('list-of-events/<int:log_id>/', ListOfEvents.as_view(), name='ListOfEvents'),
    path('search/<int:log_id>/', Search.as_view(), name='Search'),
]

