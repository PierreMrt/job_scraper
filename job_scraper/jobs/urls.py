from . import views
from django.urls import path
from jobs.views import SearchView

urlpatterns = [
    path('', views.get_job, name='home'),
    path('update', views.update_search, name='update'),
    path('searches/', views.show_searches, name='searches'),
    path('results/<str:search_key>/', views.show_results, name='results'),
    path('new-searches/', SearchView.as_view()),
]