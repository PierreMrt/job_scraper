## Rendering
from django.shortcuts import redirect
## Models
from django.db.models import Q
from .models import Search, Result
## Views
from django.views.generic import ListView
from django.views.generic.edit import CreateView
# Libs
from jobs.libs.data_analysis import TextCleaner, token_freq, lang_freq

class SearchView(ListView):
    context_object_name = 'all_searches'
    template_name = 'jobs/search_list.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('/login')
        else:
            return super().get(request)

    def get_queryset(self):
        queryset = Search.objects.filter(user=self.request.user)
        return queryset


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

        active_search = Search.objects.filter(Q(job=job), Q(country=country))
        if len(active_search) > 0:
            print('add user')
            active_search[0].user.add(self.request.user)
        else:
            print('create search')
            s = Search(job=job, country=country)
            s.save()
            s.user.add(self.request.user)
        return redirect('/')

    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('/login')
        else:
            return super().get(request)

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
        include = self.request.GET.get('include')
        exclude = self.request.GET.get('exclude')

        search_key = self.request.path.split('/')[2]
        return Result().filtered_results(search_key, include, exclude)

    def get_context_data(self, *args, **kwargs):
        context = super(ResultView, self).get_context_data(*args, **kwargs)

        search_key = self.request.path.split('/')[2]
        job = search_key.split('&&')[0].replace('_', ' ')
        country = search_key.split('&&')[1]

        keywords = get_keywords(context)
        langs = dict(get_lang_freq(context))

        info = {
            'search_key': search_key,
            'job'       : job,
            'country'   : country,
            'keywords'  : keywords,
            'langs'     : langs,
            'include'   : self.request.GET.get('include'),
            'exclude'   : self.request.GET.get('exclude')}
        context['info'] = info
        return context

def update_search(request):
    # actives = Search.objects.all() # update all searches
    actives = Search.objects.filter(user=request.user) #updates only for user
    Search().update(actives)
    return redirect('/')

def get_keywords(results):
    text_list = list([r.description for r in results['object_list']])
    full_text = ' '.join(text_list)
    tokens = TextCleaner(full_text).clean_text()
    return token_freq(tokens)

def get_lang_freq(results):
    text_list = list([r.description for r in results['object_list']])
    return lang_freq(text_list)
    
