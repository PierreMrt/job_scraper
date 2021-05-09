from django.contrib import admin

# Register your models here.
from .models import Links, Search, Results

admin.site.register(Links)
admin.site.register(Search)
admin.site.register(Results)