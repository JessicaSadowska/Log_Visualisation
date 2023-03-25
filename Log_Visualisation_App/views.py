import codecs

from django.shortcuts import render
from django.views import View
import ocel
from django.core.files.storage import FileSystemStorage


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
        }
        return render(request, 'uploaded.html', context)
    

class OcelLog:
    def __init__(self, log):
        self.log = log

    def get_events(self):
        return ocel.get_events(self.log)

    def get_objects(self):
        return ocel.get_objects(self.log)

    def objects_count(self):
        return len(ocel.get_objects(self.log))
    
