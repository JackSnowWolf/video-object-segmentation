from django.shortcuts import render,render_to_response
from django import forms
from django.http import HttpResponse
from app.models import Video
from django.core.files.storage import FileSystemStorage
import requests
import os
import json
# Create your views here.
class VideoForm(forms.Form):
    #file_field = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))
    videoname = forms.CharField()    #string
    Frame = forms.FileField()
    File = forms.FileField()     #file


url='http://127.0.0.1:5000/api/infer'


def homepage(request):

    return render_to_response('homepage.html')

def upload(request):
    if request.method == "POST":
        uf = VideoForm(request.POST, request.FILES)
        if uf.is_valid():  # if valid
            videoname = uf.cleaned_data['videoname']
            Frame = uf.cleaned_data['Frame']
            File = uf.cleaned_data['File']
            # save file
            video = Video()
            video.videoname = videoname
            video.Frame = Frame
            video.File = File
            result = video
            result.save()
            x = requests.post(url,data={"videoname":videoname},files=request.FILES)
            with open(os.path.join("app/static/video", videoname+".mp4"),"wb") as f:
                f.write(x.content)
            with open(os.path.join("app/static/headers", videoname+".json"),"w") as f:
                f.write(json.dumps(dict(x.headers)))
            v = os.path.join("/static/video", videoname+".mp4")
            h = os.path.join("/static/headers", videoname + ".json")
            x={"v":v,"h":h}
            return render_to_response('video.html',x)
    else:
        uf = VideoForm()

    return render_to_response('upload.html',{'uf':uf})


def video(request):

    return render_to_response('video.html')

def vis(request):

    return render_to_response('vis.html')

