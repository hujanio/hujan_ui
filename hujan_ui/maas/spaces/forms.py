from django import forms

class SpacesForm(forms.Form):
    name = forms.CharField()
    description = forms.TextInput()
