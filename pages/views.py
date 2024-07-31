from django.shortcuts import render
from django.http import HttpResponse
from templates.pages import Compare
from django.contrib import messages
from pages import models
# Create your views here.



def home(request):
    return render(request, "pages/home.html",{})


def spotify(request):
    if request.method == 'POST': # If the form has been submitted...
        playlists = request.POST.dict()
        play1 =playlists.get("play1")
        play2 =playlists.get("play2")
        if play1 == play2:
            return render(request,"pages/compare.html",{"badmessage":"These are the same link, Please use different spotify links!"})
        try:
            ultlist,length,biglength = Compare.getPlaylists(play1,play2)
        except:
            return render(request,"pages/compare.html",{"badmessage":"These don't seem to be spotify links. Please use a link to a spotify playlist!"})
        else:
            
            HttpResponse("pages/compared.html")
            return render(request, "pages/compared.html",{"length":length,"ultlist":ultlist,"biglength":biglength})
    else:

        return render(request, "pages/compare.html",{})
    
      


