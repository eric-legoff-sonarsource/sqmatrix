from django.shortcuts import render
from .models import Sonarqube


def index(request):
    sqversions = Sonarqube.objects.all()
    context = {'sqversions' : sqversions}
    return render(request, 'index.html', context)
