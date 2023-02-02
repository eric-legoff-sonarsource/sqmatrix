from django.shortcuts import render
from .models import Sonarqube, Plugin, Compatibility
from django.http import HttpResponseRedirect
from .forms import AddNewRelease


def index(request):
    sqversions = Sonarqube.objects.all().order_by('-full_version')
    
    compat_map ={}
    
    for v in sqversions:
        sq = Sonarqube.objects.get(full_version=v)
        complist = Compatibility.objects.all().filter(sonarqube = sq)
        compat_map[v] = complist
           
    context = {'map' : compat_map}
    return render(request, 'index.html', context)


def add(request):
    if request.method == "POST":
        form = AddNewRelease(request.POST)

        if form.is_valid():
            v = form.cleaned_data["full_version"]
            sq = Sonarqube(full_version=v)
            sq.save()

        return HttpResponseRedirect("/" )

    else:
        form = AddNewRelease()
        
        
    context = {"form" : form}
    return render(request, 'add.html', context)
