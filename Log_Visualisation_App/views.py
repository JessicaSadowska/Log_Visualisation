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
        text = ocel.get_events(log)
        context = {
            'data': text,
        }
        return render(request, 'uploaded.html', context)


