## Rendering
from django.shortcuts import redirect, render
## Models
from django.db.models import Q
from .models import Link, Search, Result
from django.contrib.auth.models import User
## HTTP & Response
from django.http import Http404, HttpResponseRedirect, HttpResponse
from rest_framework.response import Response
## Views
from rest_framework.views import APIView
from django.views.generic import ListView
from django.views.generic.edit import CreateView
from rest_framework.decorators import api_view
# Forms
from .forms import JobForm
# Libs
from jobs.libs.data_analysis import TextCleaner, token_freq, lang_freq

def get_job(request):
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = JobForm(request.POST)
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
            s.update()

    # if a GET (or any other method) we'll create a blank form
    else:
        form = JobForm()

    return render(request, 'forms.html', {'form': form})

def update_search(request):
    print('updating active searches')

    Search().update()

    return render(request, 'jobs/update.html')

class SearchView(ListView):

    queryset = Search.objects.all()
    context_object_name = 'all_searches'
    template_name = 'jobs/search_list.html'

class SearchCreateView(CreateView):

    model = Search
    fields = ['job', 'country']
    template_name = 'jobs/search_form.html'
    success_url = '/'
    
    def form_valid(self, form):
        # process the data in form.cleaned_data
        job = form.cleaned_data['job']
        country = form.cleaned_data['country']
        # here we need to pass the data to the model's methods
        job = job.replace(" ", "_").lower()
        country = country.replace(" ", "_").lower()

        s = Search(user='pierre', job=job, country=country)
        s.new_search()
        s.update()

    def form_invalid(self, form):
        response = super().form_invalid(form)
        if self.request.accepts('text/html'):
            return response
        else:
            return JsonResponse(form.errors, status=400)


class ResultView(ListView):

    model = Result
    context_object_name = 'all_results'
    template_name = 'jobs/result_list.html'

    def get_queryset(self):     
        search_key = self.request.path.split('/')[2]
        return Result().return_results(search_key)

    def get_context_data(self, *args, **kwargs):
        query = self.request.GET.get('include')
        print('QUERY', query)

        search_key = self.request.path.split('/')[2]

        job = search_key.split('&&')[0].replace('_', ' ')
        country = search_key.split('&&')[1]

        keywords = get_keywords(search_key)
        langs = dict(get_lang_freq(search_key))

        info = {
            'search_key': search_key,
            'job'       : job,
            'country'   : country,
            'keywords'  : keywords,
            'langs'     : langs}
        context = super(ResultView, self).get_context_data(*args, **kwargs)
        context['info'] = info
        return context


# def show_results(request, search_key, *args):
#     job = search_key.split('&&')[0].replace('_', ' ')
#     country = search_key.split('&&')[1]

#     # if kwargs argument include
#     # function include in models

#     # elif exclude
#     # in returned results remove ones within

#     # elif return all results

#     keywords = get_keywords(search_key)
#     langs = dict(get_lang_freq(search_key))

#     results = {}
#     results['info'] = {
#         'search_key': search_key,
#         'job'       : job,
#         'country'   : country,
#         'keywords'  : keywords,
#         'langs'     : langs}
#     results['list'] = Result().return_results(search_key)
#     return render(request, 'jobs/results.html', {'results': results})

def get_keywords(search_key):
    results = Result().return_results(search_key)
    text_list = list([r.description for r in results])
    full_text = ' '.join(text_list)
    tokens = TextCleaner(full_text).clean_text()
    return token_freq(tokens)

def get_lang_freq(search_key):
    results = Result().return_results(search_key)
    text_list = list([r.description for r in results])
    return lang_freq(text_list)
    
