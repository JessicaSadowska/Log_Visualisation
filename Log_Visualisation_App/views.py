import codecs

from django.shortcuts import render
from django.views import View
import ocel
import json
from django.core.files.storage import FileSystemStorage
# from .forms import ObjectForm


class Home(View):
    def get(self, request):
        return render(request, 'home.html')

    def post(self, request):
        file = request.FILES['uploaded_file']
        fs = FileSystemStorage(location="ciscotest/uploadedmedia")
        file = fs.save(file.name, file)
        log = ocel.import_log("ciscotest/uploadedmedia/" + file)
        ocel_log = OcelLog(log)

        context = {
            'data': ocel_log.get_events(),
            'objects_count': ocel_log.objects_count(),
            'objects': ocel_log.get_objects(),
            'event_names_string': ocel_log.get_events_names_string(),
            'event_names_array': ocel_log.get_events_names_array()
        }
        return render(request, 'uploaded.html', context)
    
    # def get_events_with_objects(request):
    #     if request.method == 'POST':
    #         form = ObjectForm(request.POST)
    #         objects = "sdf"
    #     else:
    #         form = ObjectForm()

    #     return render(request, 'uploaded.html', {'form': form, 'objects': objects})

class OcelLog:
    def __init__(self, log):
        self.log = log

    def get_events(self):
        return ocel.get_events(self.log)
    
    def get_events_names_string(self):
        events = ocel.get_events(self.log)
        return ', ' .join(list(events.keys()))
    
    def get_events_names_array(self):
        events = ocel.get_events(self.log)
        return list(events.keys())

    def get_objects(self):
        return ocel.get_objects(self.log)

    def objects_count(self):
        return len(ocel.get_objects(self.log))
                           
    def my_filtering_function(pair):
        pass
        # unwanted_key = 'Matt'
        # key, value = pair
        # if key == unwanted_key:
        #     return False  
        # else:
        #     return True
        
    def get_events_with_objects(self):
        pass

#testtesttesttest