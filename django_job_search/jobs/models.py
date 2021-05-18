from django.db import models
from django.contrib.auth.models import User
from jobs.libs.scraping import LinkedIn, Monster, Indeed

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
    user = models.CharField(max_length=255)
    job = models.CharField(max_length=255)
    country = models.CharField(max_length=255)

    def __str__(self):
        return self.search_key

    @property
    def search_key(self):
        return f'{self.job.lower()}&&{self.country.lower()}'

    @staticmethod
    def split_search_key(search_key):
        s = search_key.split('&&')
        return s[0], s[1]

    def new_search(self):
        actives = [s.search_key for s in self.active_search()]
        if self.search_key not in actives:
            self.save()
            print(f'{self.search_key} added to searches')
            Result().scrap(self.job, self.country)
        else:
            print(f'Search for {self.job} in {self.country} is already active.')
            Result().scrap(self.job, self.country)
        
    def active_search(self):
        actives = set()
        [actives.add(s) for s in Search.objects.all()]
        return actives

    def update(self):
        for active in self.active_search():
            job, country = self.split_search_key(active.search_key)
            Result().scrap(job, country)


class Result(models.Model):
    search_key = models.CharField(max_length=255)
    search = models.ForeignKey(Search, related_name='results', on_delete=models.PROTECT)
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

        linkedin = LinkedIn(cache, job, country)
        print('adding results...')
        for r in linkedin.results:
            self.add_result(r)

        # indeed = Indeed(links, cache, job, country)
        # for r in indeed.results:
        #     self.add_result(r)

        monster = Monster(links, cache, job, country)
        for r in monster.results:
            self.add_result(r)

    def cached_ids(self):
        cached_ids = set()
        result = Result.objects.all()
        [cached_ids.add(r.job_id) for r in result]
        return cached_ids

    def return_results(self, search_key):
        return Result.objects.filter(search_key=search_key)

# def main():
#     # s = Search(user='pierre', job='data_analyst', country='italy')
#     # s.new_search()
#     # Search().update()