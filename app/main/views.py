from django.shortcuts import render
from .models import Sonarqube, Plugin, Compatibility


def index(request):
    sqversions = Sonarqube.objects.all().order_by('-full_version')
    
    compat_map ={}
    
    for v in sqversions:
        sq = Sonarqube.objects.get(full_version=v)
        complist = list(Compatibility.objects.all().filter(sonarqube = sq))
        compat_map[v] = complist
        
    
    
    context = {'map' : compat_map}
    return render(request, 'index.html', context)
