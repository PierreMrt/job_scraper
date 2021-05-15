from django.db.models import Q
from django.http import Http404, HttpResponseRedirect

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
# importing user model
from django.contrib.auth.models import User

from .models import Link, Search, Result
#from .serializers import ProductSerializer, CategorySerializer

from .forms import NameForm
from django.shortcuts import render
from django.http import HttpResponse

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

            s = Search(user='pierre', job=job, country=country)
            s.new_search()

    # if a GET (or any other method) we'll create a blank form
    else:
        form = NameForm()

    return render(request, 'forms.html', {'form': form})

def update_search(request):
    print('updating active searches')

    Search().update()

    return render(request, 'update.html')

def show_searches(request):
    searches = Search().active_search()
    search_dict = {}
    for i, search  in enumerate(searches):
        search_dict[i] = {
            'search_key': search.search_key,
            'job': search.job,
            'country': search.country,
            'count': len(Result().return_results(search.search_key))}
    print(search_dict)
    
    return render(request, 'searches.html', {'context': search_dict})
    
def show_results(request, search_key):
    results = Result().return_results(search_key)
    return render(request, 'results.html', {'results': results})