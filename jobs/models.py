from django.db import models
from django.contrib.auth.models import User
from django.db.models import Q
from jobs.libs.scraping import LinkedIn, Monster, Indeed
import threading

class Link(models.Model):
    country = models.CharField(max_length=255)
    extension = models.CharField(max_length=255)
    linkedIn = models.CharField(max_length=255)
    monster = models.CharField(max_length=255)
    indeed = models.CharField(max_length=255)

    def __str__(self):
        return self.country

    def fetch(self, country):
        links = Link.objects.get(country=country)
        return (links.extension, links.monster, links.indeed)

    @staticmethod
    def populate():
        links = [
            ('italy', 'it', 'www.linkedin.com', 'https://www.monster.it/lavoro/cerca?', 'https://it.indeed.com/offerta-lavoro?'),
            ('france', 'fr', 'www.linkedin.com', 'https://www.monster.fr/emploi/recherche?', 'https://fr.indeed.com/voir-emploi?'),
            ('uruguay', 'uy', 'www.linkedin.com', 'None', 'https://uy.indeed.com/descripción-del-puesto?'),
            ('austria', 'at', 'www.linkedin.com', 'https://www.monster.at/jobs/suche?', 'https://at.indeed.com/Zeige-Job?')]
        
        for r in links:
            l = Link(country=r[0], extension=r[1], linkedIn=r[2], monster=r[3], indeed=r[4])
            l.save()


class Search(models.Model):
    user = models.ManyToManyField(User, db_column="user")
    job = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    update_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.search_key

    @property
    def search_key(self):
        return f'{self.job.lower()}&&{self.country.lower()}'

    @staticmethod
    def split_search_key(search_key):
        s = search_key.split('&&')
        return s[0], s[1]

    def update(self, searches):
        for search in searches:
            job, country = self.split_search_key(search.search_key)
            Result().scrap(job, country)


class Result(models.Model):
    search_key = models.CharField(max_length=255)
    search = models.ForeignKey(Search, related_name='results', on_delete=models.CASCADE)
    source = models.CharField(max_length=255, null=True, blank=True)
    job_id = models.CharField(max_length=255, null=True, blank=True)
    job_title = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    company = models.CharField(max_length=255, null=True, blank=True)
    location = models.CharField(max_length=255, null=True, blank=True)
    country = models.CharField(max_length=255, null=True, blank=True)
    date = models.DateTimeField(null=True, blank=True)
    link = models.CharField(max_length=255)

    def __str__(self):
        return self.search_key

    def add_result(self, r):
        search_key = r['search_key']
        job, country = Search().split_search_key(search_key)
        search = Search.objects.filter(job=job, country=country).get()
        
        new_entry = Result.objects.create(search_key=r['search_key'], search=search, source=r['source'], job_id=r['job_id'], job_title=r['job_title'], 
                            description=r['description'], company=r['company'], location=r['location'],
                            country=r['country'], date=r['date'], link=r['link'])
        new_entry.save()

    def scrap(self, job, country):
        links = Link().fetch(country)
        cache = self.cached_ids()
        print(f"Scraping {job} in {country}.")

        t1 = threading.Thread(target=self.scrap_linkedin,args=(cache, job, country,))
        t1.start()

        t2 = threading.Thread(target=self.scrap_monster,args=(links, cache, job, country,))
        t2.start()

        t1.join()
        t2.join()

    def scrap_linkedin(self, cache, job, country):
        linkedin = LinkedIn(cache, job, country)
        for r in linkedin.results:
            self.add_result(r)
    
    def scrap_monster(self, links, cache, job, country):
        monster = Monster(links, cache, job, country)
        try:
            for r in monster.results:
                self.add_result(r)
        except AttributeError:
            print(f"Skipping monster as {country} doesn't have it.")


    def cached_ids(self):
        cached_ids = set()
        result = Result.objects.all()
        [cached_ids.add(r.job_id) for r in result]
        return cached_ids
    
    def filtered_results(self, search_key, include, exclude):
        results = Result.objects.filter(search_key=search_key)
        if include is not None and include != '':
            to_include = include.split(', ')
            for kw in to_include:
                    results = results.filter(Q(description__contains=kw) | Q(job_title__contains=kw) | Q(location__contains=kw) | Q(company__contains=kw))
        if exclude is not None and exclude != '':
            print('EXCLUDE: ', exclude )
            to_exclude = exclude.split(', ')
            for kw in to_exclude:
                results = results.exclude(Q(description__contains=kw) | Q(job_title__contains=kw) | Q(location__contains=kw) | Q(company__contains=kw))  
        return results.order_by('-date')


def main():
    Result().filtered_results('data_analyst&&france', include='python, SQL')