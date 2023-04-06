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

        events = ocel.get_events(ocel_log)
        log_objects = ocel.get_objects(ocel_log)
        attribute_names = ocel.get_attribute_names(ocel_log)
        object_types = ocel.get_object_types(ocel_log)

        events_count = len(events)
        objects_count = len(log_objects)

        log = OcelLog(events_count=events_count, objects_count=objects_count,
                      object_types=object_types, attribute_names=attribute_names)
        log.save()

        for obj, value in log_objects.items():
            o = LogObject(ocel_log=log, name=obj, type=value['ocel:type'],
                          ovmap=value['ocel:ovmap'])
            o.save()

        activities = []

        for event, value in events.items():
            e = Event(ocel_log=log, name=event, activity=value['ocel:activity'],
                      timestamp=value['ocel:timestamp'], vmap=value['ocel:vmap'])
            e.save()

            if value['ocel:activity'] not in activities:
                activities.append(value['ocel:activity'])

            for obj in value['ocel:omap']:
                print(f"OBJECT NAME:", obj)
                o = LogObject.objects.get(ocel_log=log, name=obj)
                e.event_objects.add(o)
            e.save()

        log.activities = activities
        log.save()

        set_of_events = log.event_set.all()
        set_of_objects = log.logobject_set.all()

        context = {
            'events': set_of_events,
            'objects': set_of_objects,
            'log': log,
        }
        return render(request, 'uploaded.html', context)


class LogsWithEventName(View):
    def post(self, request, log_id):
        log = OcelLog.objects.get(id=log_id)
        event_name = request.POST['event']
        event = Event.objects.get(ocel_log=log, name=event_name)

        context = {
            'event': event
        }
        return render(request, 'uploaded_logs_with_event_name.html', context)


class LogsWithActivity(View):
    def post(self, request, log_id):
        log = OcelLog.objects.get(id=log_id)
        activity = request.POST['activity']
        events = Event.objects.filter(ocel_log=log, activity=activity)

        context = {
            "activity": activity,
            "events": events,
        }
        return render(request, 'uploaded_logs_with_activity.html', context)


class LogsWithObject(View):
    def post(self, request, log_id):
        log = OcelLog.objects.get(id=log_id)
        object_name = request.POST['object']
        log_object = LogObject.objects.get(ocel_log=log, name=object_name)
        events = log_object.events.all()

        context = {
            "object": log_object,
            "events": events,
        }
        return render(request, 'uploaded_logs_with_object.html', context)


class LogsWithObjectType(View):
    def post(self, request, log_id):
        log = OcelLog.objects.get(id=log_id)
        object_type = request.POST['object_type']
        log_objects = LogObject.objects.filter(ocel_log=log, type=object_type)

        events = []

        for obj in log_objects:
            obj_events = obj.events.all()
            for e in obj_events:
                if e not in events:
                    events.append(e)

        context = {
            "object_type": object_type,
            "objects": log_objects,
            "events": events,
        }
        return render(request, 'uploaded_logs_with_object_type.html', context)





















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
