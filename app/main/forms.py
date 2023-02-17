from django import forms


class AddNewRelease(forms.Form):
     # Label is the text that shows before the input-box
   full_version = forms.CharField(label="SonarQube version", max_length=150,
                           widget= forms.TextInput
                           (attrs={'placeholder':'full version number'}))
   
   
class CompareReleases(forms.Form):
  v1 = forms.CharField(label="SonarQube from version", max_length=150,
                           widget= forms.TextInput
                           (attrs={'placeholder':'from version number'}))
  v2 = forms.CharField(label="SonarQube to version", max_length=150,
                           widget= forms.TextInput
                           (attrs={'placeholder':'to version number'})) 