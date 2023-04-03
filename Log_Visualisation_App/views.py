import codecs

from django.shortcuts import render
from django.views import View
import ocel
from django.core.files.storage import FileSystemStorage
# from .forms import ObjectForm
from Log_Visualisation_App.models import OcelLog, Event, LogObject


class Home(View):
    def get(self, request):
        return render(request, 'home.html')

    def post(self, request):
        file = request.FILES['uploaded_file']
        fs = FileSystemStorage(location="ciscotest/uploadedmedia")
        file = fs.save(file.name, file)
        ocel_log = ocel.import_log("ciscotest/uploadedmedia/" + file)
        log = OcelLog(log=ocel_log)
        log.save()

        events = ocel.get_events(ocel_log)
        for event, value in events.items():
            e = Event(ocel_log=log, event_name=event, event_value=value)
            e.save()
        set_of_events = log.event_set.all()

        log_objects = ocel.get_objects(ocel_log)
        for obj in log_objects:
            o = LogObject(ocel_log=log, object_name=obj)
            o.save()
        set_of_objects = log.logobject_set.all()

        log.events_count = len(events)
        log.objects_count = len(log_objects)
        log.save()

        context = {
            'events': set_of_events,
            'objects': set_of_objects,
            'log': log,
            'data': events,
            # 'objects': log.get_objects(),
        }
        return render(request, 'uploaded.html', context)


class UploadedLogsWithObject(View):
    def post(self, request, log_id):
        log = OcelLog.objects.get(id=log_id)
        object_name = request.POST['object']
        log_object = LogObject.objects.get(ocel_log=log, object_name=object_name)

        context = {
            'object': log_object,
            'log': log,
            # 'data': log.get_events(),
            # 'objects_count': log.objects_count(),
            # 'objects': log.get_objects(),
            # 'event_names_string': log.get_events_names_string(),
            # 'event_names_array': log.get_events_names_array(),
            # 'events_count': log.events_count(),
        }
        return render(request, 'uploaded_logs_with_object.html', context)


class UploadedLogsWithEventName(View):
    def post(self, request, log_id):
        log = OcelLog.objects.get(id=log_id)
        event_name = request.POST['event']
        event = Event.objects.get(ocel_log=log, event_name=event_name)

        context = {
            'event': event,
            'log': log,
            # 'data': log.get_events(),
            # 'objects_count': log.objects_count(),
            # 'objects': log.get_objects(),
            # 'event_names_string': log.get_events_names_string(),
            # 'event_names_array': log.get_events_names_array(),
            # 'events_count': log.events_count(),
        }
        return render(request, 'uploaded_logs_with_event_name.html', context)


















    # def get_events_with_objects(request):
    #     if request.method == 'POST':
    #         form = ObjectForm(request.POST)
    #         objects = "sdf"
    #     else:
    #         form = ObjectForm()

    #     return render(request, 'uploaded.html', {'form': form, 'objects': objects})

# class OcelLog:
#     def __init__(self, log):
#         self.log = log
#
#     def get_events(self):
#         return ocel.get_events(self.log)
#
#     def get_events_names_string(self):
#         events = ocel.get_events(self.log)
#         return ', ' .join(list(events.keys()))
#
#     def get_events_names_array(self):
#         events = ocel.get_events(self.log)
#         return list(events.keys())
#
#     def get_objects(self):
#         return ocel.get_objects(self.log)
#
#     def objects_count(self):
#         return len(ocel.get_objects(self.log))
#
#     def my_filtering_function(pair):
#         pass
#         # unwanted_key = 'Matt'
#         # key, value = pair
#         # if key == unwanted_key:
#         #     return False
#         # else:
#         #     return True
#
#     def get_events_with_objects(self):
#         pass
#
