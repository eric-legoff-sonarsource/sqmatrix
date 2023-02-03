from django.shortcuts import render
from .models import Sonarqube, Plugin, Compatibility
from django.http import HttpResponseRedirect
from .forms import AddNewRelease
import collections
import distutils


def releases(request):
    sqversions = Sonarqube.objects.all().order_by('-full_version')
    
    compat_map ={}
    
    for v in sqversions:
        sq = Sonarqube.objects.get(full_version=v)
        complist = Compatibility.objects.all().filter(sonarqube = sq)
        compat_map[v] = complist
        
        
    map = collections.OrderedDict(sorted(compat_map.items(), reverse=True))
    context = {'map' : map}
    return render(request, 'releases.html', context)


def semsort(item):
    major, minor,patch,build = item[0].split('.')   
    return (int(major), int(minor), int(patch), int(build))


def plugins(request):
    comps = list(Compatibility.objects.all().order_by('plugin__name'))
    
    plugin_map ={}
   
    for c in comps:
        if c.plugin.name in plugin_map:
            m = plugin_map[c.plugin.name]
            if c.version in m:
                m[c.version].append(c.sonarqube)
                plugin_map[c.plugin.name]=m             
            else:
                m[c.version]=[c.sonarqube]
                plugin_map[c.plugin.name] = m
        else:
            plugin_map[c.plugin.name]={c.version : [c.sonarqube]}
            
    map = {}     
    for k in plugin_map.keys():
        od = collections.OrderedDict(sorted(plugin_map[k].items(), key = semsort, reverse=True)) 
        map[k] = od       
                     
    context = {'map' : map}
    return render(request, 'plugins.html', context)


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
