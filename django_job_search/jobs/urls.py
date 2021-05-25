from . import views
from django.urls import path
from jobs.views import SearchView, SearchCreateView, ResultView


urlpatterns = [
    path('', SearchView.as_view(), name='home'),
    path('add/', SearchCreateView.as_view()),
    path('update', views.update_search, name='update'),
    # path('results/<str:search_key>/', views.create_form, name='results'),
    # path('results/<str:search_key>/', views.show_results, name='results'),
    path('results/<str:search_key>/', ResultView.as_view(), name='results'),
]