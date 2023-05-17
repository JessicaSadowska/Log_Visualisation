import ocel
from django.db import models


class OcelLog(models.Model):
    events_count = models.IntegerField(null=True)
    objects_count = models.IntegerField(null=True)
    object_types = models.JSONField(null=True)
    attribute_names = models.JSONField(null=True)
    activities = models.JSONField(null=True)


class LogObject(models.Model):
    ocel_log = models.ForeignKey(OcelLog, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=255)
    ovmap = models.TextField(null=True)

    def __str__(self):
        return f"{self.name}"


class Event(models.Model):
    ocel_log = models.ForeignKey(OcelLog, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    activity = models.CharField(max_length=255)
    timestamp = models.DateTimeField()
    event_objects = models.ManyToManyField(LogObject, related_name="events")
    vmap = models.JSONField(null=True)

    def __str__(self):
        return f"{self.name}"

