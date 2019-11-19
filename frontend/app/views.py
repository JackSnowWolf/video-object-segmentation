from django.shortcuts import render,render_to_response
from django import forms
from django.http import HttpResponse
from app.models import Video
# Create your views here.
class VideoForm(forms.Form):
    videoname = forms.CharField()    #string
    File = forms.FileField()     #file

def homepage(request):
    if request.method == "POST":
        uf = VideoForm(request.POST, request.FILES)
        if uf.is_valid():  # if valid
            videoname = uf.cleaned_data['videoname']
            File = uf.cleaned_data['headFile']
            # save file
            video = Video()
            video.videoname = videoname
            video.File = File
            video.save()
            return HttpResponse('upload successfully!')
    else:
        uf = VideoForm()

    return render_to_response('homepage.html',{'uf':uf})