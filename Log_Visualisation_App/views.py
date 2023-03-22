import codecs

from django.shortcuts import render
from django.views import View


class Home(View):
    def get(self, request):
        return render(request, 'home.html')

    def post(self, request):
        file = request.FILES['uploaded_file']
        text = file.read()
        # fs = FileSystemStorage(location="ciscotest/uploadedmedia")
        # filename = fs.save(myfile.name, myfile)
        # uploaded_file_url = fs.url(filename)
        # f = codecs.open(file, encoding='utf-8')
        # data = f.read()
        context = {
            'data': text,
        }
        return render(request, 'uploaded.html', context)


