from django.db import models

# Create your models here.


class Users(models.Model):
    username = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)


class Links(models.Model):
    country = models.CharField(max_length=255)
    extension = models.CharField(max_length=255)
    linkedIn = models.CharField(max_length=255)
    monster = models.CharField(max_length=255)
    indeed = models.CharField(max_length=255)


class Search(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    job = models.CharField(max_length=255)
    country = models.ForeignKey(Links, on_delete=models.CASCADE)
    search_key = models.CharField(max_length=255)


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

