from django import forms

class JobForm(forms.Form):
    job = forms.CharField(label='Job', max_length=100)
    country = forms.CharField(label='Country', max_length=100)
    
class FilterForm(forms.Form):
    include = forms.CharField(label='Include', max_length=100)
    exclude = forms.CharField(label='Exclude', max_length=100)