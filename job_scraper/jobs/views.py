from django.db.models import Q
from django.http import Http404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view

from .models import Links, Search, Results
# from .serializers import ProductSerializer, CategorySerializer

from django.shortcuts import render

def forms(request):
    return render(request, 'forms.html', {'title': 'Forms'})
