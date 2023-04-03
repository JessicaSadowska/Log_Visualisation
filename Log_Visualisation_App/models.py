import ocel
from django.db import models


class OcelLog(models.Model):
    log = models.TextField()

    def get_events(self):
        return ocel.get_events(self.log)

    def get_events_names_string(self):
        events = ocel.get_events(self.log)
        return ', '.join(list(events.keys()))

    def get_events_names_array(self):
        events = ocel.get_events(self.log)
        return list(events.keys())

    def events_count(self):
        return len(ocel.get_events(self.log))

    def get_objects(self):
        return ocel.get_objects(self.log)

    def objects_count(self):
        return len(ocel.get_objects(self.log))
