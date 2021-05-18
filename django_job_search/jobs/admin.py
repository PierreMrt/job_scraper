from django.contrib import admin

# Register your models here.
from .models import Link, Search, Result

admin.site.register(Link)
admin.site.register(Search)
admin.site.register(Result)