from django.db import models
# importation de user depuis Django
from django.contrib.auth.models import User



# Create your models here.

# Pas besoin de créer la class Users, elle existe déjà
# avec l'aide de Django
#class Users(models.Model):
#    username = models.CharField(max_length=255)
#    email = models.CharField(max_length=255)
#    password = models.CharField(max_length=255)


class Links(models.Model):
    country = models.CharField(max_length=255)
    extension = models.CharField(max_length=255)
    linkedIn = models.CharField(max_length=255)
    monster = models.CharField(max_length=255)
    indeed = models.CharField(max_length=255)
# C'est à cet endroit que l'on ajoute les fonctions pour afficher les infos dans l'API.

class Search(models.Model):
    ## j'ai importé User des modèles pré-fabriqués de Django
    ## tous les champs & méthodes sont dans la documentation :
    ## https://docs.djangoproject.com/fr/3.1/ref/contrib/auth/
    user = models.CharField(max_length=255)
    job = models.CharField(max_length=255)
    country = models.CharField(max_length=255)

    @property
    def search_key(self):
        return f'{self.job.lower()}&&{self.country.lower()}'

    def new_search(self):
        actives = self.active_search()
        if self.search_key not in actives:
            self.save()
            print('added to db')
        else:
            print(f'Search for {self.job} in {self.country} is already active.')
        
    def active_search(self):
        actives = set()
        [actives.add(s.search_key) for s in Search.objects.all()]
        return actives


class Results(models.Model):
    search_key = models.ForeignKey(Search, on_delete=models.CASCADE)
    source = models.CharField(max_length=255)
    job_id = models.CharField(max_length=255)
    job_title = models.CharField(max_length=255)
    description = models.TextField()
    company = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    date = models.DateTimeField()
    link = models.CharField(max_length=255)

