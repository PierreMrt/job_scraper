from django.db.models import Q
from django.http import Http404, HttpResponseRedirect

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
# importing user model
from django.contrib.auth.models import User

<<<<<<< HEAD
from .models import Links, Search, Results
#from .serializers import ProductSerializer, CategorySerializer
=======
from .models import Link, Search, Result
# from .serializers import ProductSerializer, CategorySerializer
>>>>>>> 9ec63b93746965e82df8dc87452000d11ca97586

from .forms import NameForm
from django.shortcuts import render

def get_job(request):
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = NameForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data
            job = form.cleaned_data['job']
            country = form.cleaned_data['country']
            # here we need to pass the data to the model's methods
            job = job.replace(" ", "_").lower()
            country = country.replace(" ", "_").lower()
<<<<<<< HEAD
=======

>>>>>>> 9ec63b93746965e82df8dc87452000d11ca97586
            s = Search(0, job, country)
            s.new_search()

    # if a GET (or any other method) we'll create a blank form
    else:
        form = NameForm()

    return render(request, 'forms.html', {'form': form})