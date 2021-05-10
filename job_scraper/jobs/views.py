from django.db.models import Q
from django.http import Http404, HttpResponseRedirect

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view

from .models import Links, Search, Results
# from .serializers import ProductSerializer, CategorySerializer

from .forms import NameForm
from django.shortcuts import render

def get_job(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = NameForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            job = form.cleaned_data['job']
            country = form.cleaned_data['country']
            create_new_search(job, country)
            # redirect to a new URL:
            # return render(name)

    # if a GET (or any other method) we'll create a blank form
    else:
        form = NameForm()

    return render(request, 'forms.html', {'form': form})