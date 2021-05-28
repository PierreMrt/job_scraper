from jobs.models import Result
from . import views
from django.urls import path
from jobs.views import SearchView, SearchCreateView, ResultView


urlpatterns = [
    path('', SearchView.as_view(), name='home'),
    path('add/', SearchCreateView.as_view()),
    path('update/', views.update_search, name='update'),
    path('delete_search/', views.DeleteSearchView.as_view(), name='delete'),
    path(f'results/<str:search_key>/', ResultView.as_view(), name='filtered_results'),
]