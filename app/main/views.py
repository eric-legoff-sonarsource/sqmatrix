from django.shortcuts import render
from .models import Sonarqube


def index(request):
    sqversions = Sonarqube.objects.all().order_by('-full_version')
    context = {'sqversions' : sqversions}
    return render(request, 'index.html', context)
