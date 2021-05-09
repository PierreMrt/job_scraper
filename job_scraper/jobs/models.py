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
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    job = models.CharField(max_length=255)
    country = models.ForeignKey(Links, on_delete=models.CASCADE)
    search_key = models.CharField(max_length=255)

    def create_new_search(self, job, country):
        job = self.job.lower()
        country = self.country.lower()

        self.search_key = f'{job}&&{country}'

        db = SqlConnexion(DB_NAME)
        actives = get_active_search(db)
        if self.search_key not in actives:
            row = ('pierre', job, country, self.search_key)
            db.curr.execute("INSERT INTO search values (NULL, ?, ?, ?, ?)", row)
            scrap(db, job, country)
        else:
            print(f'Search for {job} in {country} is already active.')

        # df = db.db_to_panda(search_key)
        # print(df)
        db.conn.close()


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

