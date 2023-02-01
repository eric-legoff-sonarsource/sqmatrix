from django import forms


class AddNewRelease(forms.Form):
     # Label is the text that shows before the input-box
   full_version = forms.CharField(label="SonarQube version", max_length=150,
                           widget= forms.TextInput
                           (attrs={'placeholder':'e.g 8.8.0.42792'}))