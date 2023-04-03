import ocel
from django.db import models


class OcelLog(models.Model):
    log = models.TextField()
    events_count = models.IntegerField(null=True)
    objects_count = models.IntegerField(null=True)

    def get_events_names_string(self):
        events = ocel.get_events(self.log)
        return ', '.join(list(events.keys()))

    def get_events_names_array(self):
        events = ocel.get_events(self.log)
        return list(events.keys())


class Event(models.Model):
    ocel_log = models.ForeignKey(OcelLog, on_delete=models.CASCADE)
    event_name = models.CharField(max_length=255)
    event_value = models.TextField()


class LogObject(models.Model):
    ocel_log = models.ForeignKey(OcelLog, on_delete=models.CASCADE)
    object_name = models.CharField(max_length=255)
