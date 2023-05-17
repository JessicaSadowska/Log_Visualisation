from django.shortcuts import render
from django.views import View
import ocel
from django.core.files.storage import FileSystemStorage
import json
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
    def get(self, request, log_id, event_name):
        log = OcelLog.objects.get(id=log_id)
        event = Event.objects.get(ocel_log=log, name=event_name)

        context = {
            'event': event,
            'log': log,
        }
        return render(request, 'uploaded_logs_with_event_name.html', context)

    # def post(self, request, log_id):
    #     log = OcelLog.objects.get(id=log_id)
    #     event_name = request.POST['event']
    #     event = Event.objects.get(ocel_log=log, name=event_name)
    #
    #     context = {
    #         'event': event
    #     }
    #     return render(request, 'uploaded_logs_with_event_name.html', context)


class LogsWithActivity(View):
    def get(self, request, log_id, activity):
        log = OcelLog.objects.get(id=log_id)
        events = Event.objects.filter(ocel_log=log, activity=activity)

        context = {
            "activity": activity,
            "events": events,
            'log': log,
        }
        return render(request, 'uploaded_logs_with_activity.html', context)

    # def post(self, request, log_id):
    #     log = OcelLog.objects.get(id=log_id)
    #     activity = request.POST['activity']
    #     events = Event.objects.filter(ocel_log=log, activity=activity)
    #
    #     context = {
    #         "activity": activity,
    #         "events": events,
    #     }
    #     return render(request, 'uploaded_logs_with_activity.html', context)


class LogsWithObject(View):
    def get(self, request, log_id, object_id):
        log = OcelLog.objects.get(id=log_id)
        log_object = LogObject.objects.get(id=object_id, ocel_log=log)
        events = log_object.events.all()

        context = {
            "object": log_object,
            "events": events,
            'log': log,
        }
        return render(request, 'uploaded_logs_with_object.html', context)

    # def post(self, request, log_id):
    #     log = OcelLog.objects.get(id=log_id)
    #     object_name = request.POST['object']
    #     log_object = LogObject.objects.get(ocel_log=log, name=object_name)
    #     events = log_object.events.all()
    #
    #     context = {
    #         "object": log_object,
    #         "events": events,
    #     }
    #     return render(request, 'uploaded_logs_with_object.html', context)


class LogsWithObjectType(View):
    def get(self, request, log_id, object_type):
        log = OcelLog.objects.get(id=log_id)
        object_type = object_type
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
            'log': log,
        }
        return render(request, 'uploaded_logs_with_object_type.html', context)

    # def post(self, request, log_id):
    #     log = OcelLog.objects.get(id=log_id)
    #     object_type = request.POST['object_type']
    #     log_objects = LogObject.objects.filter(ocel_log=log, type=object_type)
    #
    #     events = []
    #
    #     for obj in log_objects:
    #         obj_events = obj.events.all()
    #         for e in obj_events:
    #             if e not in events:
    #                 events.append(e)
    #
    #     context = {
    #         "object_type": object_type,
    #         "objects": log_objects,
    #         "events": events,
    #     }
    #     return render(request, 'uploaded_logs_with_object_type.html', context)


class DrawTable(View):
    def get(self, request, log_id):
        log = OcelLog.objects.get(id=log_id)
        events = log.event_set.all()
        objects = log.logobject_set.all()

        ordered_events = events.order_by('timestamp')
        data = []

        for obj in objects:
            row = []
            for event in ordered_events:
                if obj in event.event_objects.all():
                    row.append(1)
                else:
                    row.append(0)
            data.append({obj.name: row})

        context = {
            "events": ordered_events,
            "data": data,
        }
        return render(request, 'draw.html', context=context)


class DrawDependenciesOfObjects(View):
    def get(self, request, log_id, object_id):

        log = OcelLog.objects.get(id=log_id)
        events = log.event_set.all()
        objects = log.logobject_set.all()
        desired_object = objects.get(id=object_id)

        ordered_events = events.order_by('timestamp')

        first_event_with_desired_object = None
        events_in_graph = []

        for event in ordered_events:
            if desired_object in event.event_objects.all():
                first_event_with_desired_object = event
                events_in_graph.append(event)
                break

        first_layer_objects = []
        related_objects0 = {}
        second_layer_objects = {}
        third_layer_objects = {}

        for obj in first_event_with_desired_object.event_objects.all():
            first_layer_objects.append(obj.name)
            for event in ordered_events:
                if obj in event.event_objects.all() and event.timestamp >= first_event_with_desired_object.timestamp:
                    try:
                        related_objects0[event.name] = [obj.name for obj in event.event_objects.all()]
                    except:
                        pass

        ev_list = []
        for key in related_objects0.keys():
            e = events.get(name=key)
            ev_list.append(e)

        ev_list.sort(key=lambda x: x.timestamp, reverse=False)

        related_objects = {}
        for i in ev_list:
            related_objects[i.name] = [obj.name for obj in i.event_objects.all()]

        related_objects.pop(first_event_with_desired_object.name)

        for obj in first_event_with_desired_object.event_objects.all():
            objects_on_arrow = [obj.name]
            for key, val in related_objects.items():
                if obj.name in val and ordered_events.get(
                        name=key).timestamp > first_event_with_desired_object.timestamp:
                    try:
                        ev = ordered_events.get(name=key)
                        text = f"{ev.name}: {ev.activity}"
                        if key not in second_layer_objects.keys():
                            second_layer_objects[key] = [val, text, objects_on_arrow]
                        else:
                            second_layer_objects[key][2].append(obj.name)
                        if ordered_events.get(name=key) not in events_in_graph:
                            events_in_graph.append(ordered_events.get(name=key))
                        break
                    except:
                        pass

        for key in second_layer_objects.keys():
            related_objects.pop(key)

        for key, value in second_layer_objects.items():
            inside_layer = {}
            for obj in value[0]:
                for k, val in related_objects.items():
                    if obj in val and ordered_events.get(
                            name=key).timestamp > first_event_with_desired_object.timestamp:
                        try:
                            ev = ordered_events.get(name=k)
                            text = f"{ev.name}: {ev.activity}"
                            objects_on_arrow = [obj]
                            if k + key not in inside_layer.keys():
                                inside_layer[k + key] = [val, text, objects_on_arrow]
                            else:
                                inside_layer[k + key][2].append(obj)

                            print(f"THIRD LAYER KEY: {k + key}")
                            print(f"THIRD LAYER KEY: {inside_layer[k + key]}")
                            if ordered_events.get(name=k) not in events_in_graph:
                                events_in_graph.append(ordered_events.get(name=k))
                            break
                        except:
                            pass
            third_layer_objects[key] = inside_layer

        first_layer_objects_json = json.dumps(first_layer_objects)
        second_layer_objects_json = json.dumps(second_layer_objects)
        third_layer_objects_json = json.dumps(third_layer_objects)

        context = {
            "event_with_desired_object": first_event_with_desired_object,
            "first_layer_objects": first_layer_objects_json,
            "second_layer_objects": second_layer_objects_json,
            "third_layer_objects": third_layer_objects_json,
            "events_in_graph": events_in_graph,
            "log": log,
            "objects": objects,
        }

        return render(request, 'draw_dependencies.html', context=context)


class DrawAnotherDependencies(View):
    def get(self, request, log_id, event_name):

        log = OcelLog.objects.get(id=log_id)
        events = log.event_set.all()
        objects = log.logobject_set.all()

        ordered_events = events.order_by('timestamp')

        first_event_with_desired_object = log.event_set.all().get(name=event_name)
        events_in_graph = []
        events_in_graph.append(first_event_with_desired_object)

        first_layer_objects = []
        related_objects0 = {}
        second_layer_objects = {}
        third_layer_objects = {}

        for obj in first_event_with_desired_object.event_objects.all():
            first_layer_objects.append(obj.name)
            for event in ordered_events:
                if obj in event.event_objects.all() and event.timestamp >= first_event_with_desired_object.timestamp:
                    try:
                        related_objects0[event.name] = [obj.name for obj in event.event_objects.all()]
                    except:
                        pass

        ev_list = []
        for key in related_objects0.keys():
            e = events.get(name=key)
            ev_list.append(e)

        ev_list.sort(key=lambda x: x.timestamp, reverse=False)

        related_objects = {}
        for i in ev_list:
            related_objects[i.name] = [obj.name for obj in i.event_objects.all()]

        related_objects.pop(first_event_with_desired_object.name)

        for obj in first_event_with_desired_object.event_objects.all():
            objects_on_arrow = [obj.name]
            for key, val in related_objects.items():
                if obj.name in val and ordered_events.get(name=key).timestamp > first_event_with_desired_object.timestamp:
                    try:
                        ev = ordered_events.get(name=key)
                        text = f"{ev.name}: {ev.activity}"
                        if key not in second_layer_objects.keys():
                            second_layer_objects[key] = [val, text, objects_on_arrow]
                        else:
                            second_layer_objects[key][2].append(obj.name)
                        if ordered_events.get(name=key) not in events_in_graph:
                            events_in_graph.append(ordered_events.get(name=key))
                        break
                    except:
                        pass

        for key in second_layer_objects.keys():
            related_objects.pop(key)

        for key, value in second_layer_objects.items():
            inside_layer = {}
            for obj in value[0]:
                for k, val in related_objects.items():
                    if obj in val and ordered_events.get(name=key).timestamp > first_event_with_desired_object.timestamp:
                        try:
                            ev = ordered_events.get(name=k)
                            text = f"{ev.name}: {ev.activity}"
                            objects_on_arrow = [obj]
                            if k+key not in inside_layer.keys():
                                inside_layer[k+key] = [val, text, objects_on_arrow]
                            else:
                                inside_layer[k+key][2].append(obj)

                            print(f"THIRD LAYER KEY: {k+key}")
                            print(f"THIRD LAYER KEY: {inside_layer[k+key]}")
                            if ordered_events.get(name=k) not in events_in_graph:
                                events_in_graph.append(ordered_events.get(name=k))
                            break
                        except:
                            pass
            third_layer_objects[key] = inside_layer

        first_layer_objects_json = json.dumps(first_layer_objects)
        second_layer_objects_json = json.dumps(second_layer_objects)
        third_layer_objects_json = json.dumps(third_layer_objects)

        context = {
            "event_with_desired_object": first_event_with_desired_object,
            "first_layer_objects": first_layer_objects_json,
            "second_layer_objects": second_layer_objects_json,
            "third_layer_objects": third_layer_objects_json,
            "events_in_graph": events_in_graph,
            "log": log,
            "objects": objects,
        }

        return render(request, 'draw_dependencies.html', context=context)


class Statistics(View):
    def get(self, request, log_id):
        log = OcelLog.objects.get(id=log_id)
        events = log.event_set.all()
        objects = log.logobject_set.all()

        context = {
            'events': events,
            'objects': objects,
            'log': log,
        }
        return render(request, 'statistics.html', context)


class Graphs(View):
    def get(self, request, log_id):
        log = OcelLog.objects.get(id=log_id)
        events = log.event_set.all()
        objects = log.logobject_set.all()

        context = {
            'events': events,
            'objects': objects,
            'log': log,
        }
        return render(request, 'graphs.html', context)


class GraphsUploaded(View):
    def get(self, request, log_id, object_id):
        log = OcelLog.objects.get(id=log_id)
        events = log.event_set.all()
        objects = log.logobject_set.all()

        context = {
            'events': events,
            'objects': objects,
            'log': log,
        }
        return render(request, 'graphs_uploaded.html', context)


class ListOfEvents(View):
    def get(self, request, log_id):
        log = OcelLog.objects.get(id=log_id)
        events = log.event_set.all()
        objects = log.logobject_set.all()

        context = {
            'events': events,
            'objects': objects,
            'log': log,
        }
        return render(request, 'list_of_events.html', context)


class Search(View):
    def get(self, request, log_id):
        log = OcelLog.objects.get(id=log_id)
        events = log.event_set.all()
        objects = log.logobject_set.all()

        context = {
            'events': events,
            'objects': objects,
            'log': log,
        }
        return render(request, 'search.html', context)
