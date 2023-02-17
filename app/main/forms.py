from django import forms
from .models import Sonarqube




class AddNewRelease(forms.Form):
  
     # Label is the text that shows before the input-box
   full_version = forms.CharField(label="SonarQube version", max_length=150,
                           widget= forms.TextInput
                           (attrs={'placeholder':'full version number'}))
   
   
class CompareReleases(forms.Form):
  sqversions = Sonarqube.objects.all().order_by('-full_version')
  CHOICES = []
  for s in sqversions:
    CHOICES.append((s.full_version,s.full_version))
  
  v1 = forms.CharField(label="SonarQube from version", max_length=150,
                           widget= forms.Select(choices=CHOICES[1:]))
  v2 = forms.CharField(label="SonarQube to version", max_length=150,
                           widget= forms.Select(choices=CHOICES)) 
  


