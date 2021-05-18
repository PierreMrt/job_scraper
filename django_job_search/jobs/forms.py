from django import forms

class JobForm(forms.Form):
    job = forms.CharField(label='Job', max_length=100, widget=forms.TextInput(attrs={'class': "form-control"}))
    country = forms.CharField(label='Country', max_length=100)