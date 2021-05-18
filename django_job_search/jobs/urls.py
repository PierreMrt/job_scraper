from . import views
from django.urls import path
from jobs.views import SearchView, SearchCreateView

urlpatterns = [
    # path('', views.get_job, name='home'),
    path('', SearchView.as_view()),
    path('add/', SearchCreateView.as_view()),
    path('update', views.update_search, name='update'),
    # path('searches/', views.show_searches, name='searches'),
    path('results/<str:search_key>/', views.show_results, name='results'),
]