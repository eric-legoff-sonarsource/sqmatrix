from django import forms


class AddNewRelease(forms.Form):
    full_version = forms.CharField(label="full_version", max_length=30)  # Label is the text that shows before the input-box
   