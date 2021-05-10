from django import forms

class NameForm(forms.Form):
    job = forms.CharField(label='Job', max_length=100)
    country = forms.CharField(label='Country', max_length=100)