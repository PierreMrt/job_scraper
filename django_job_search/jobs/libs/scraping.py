from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import requests
import re
from datetime import datetime, timedelta
from django.utils import timezone

DATE = datetime.now(tz=timezone.utc)

class Scraper:
    def __init__(self, cache, job_title, location):
        self.cache = cache

        self.location = location
        self.job_title = job_title

    def _get_ids(self):
        job_ids = set()
        content = selenium_content(self.results_page_url)
        if content.find('div', class_='h-captcha') is not None:
            print('captcha')
        else:
            jobs = content.find_all(self.id_param['tag'], class_=self.id_param['class'])
            for job in jobs:
                job_ids.add(job.attrs[self.id_param['attr']])
        return job_ids

    def _fetch_details(self, content, job_details):
        for key, param in job_details.items():
            try:
                job_details[key] = content.find(param['tag'], class_=param['class']).text
            except AttributeError as e:
                job_details[key] = ""
        
        return job_details

    def transform_date(self, raw_date):
        try:
            rgx = re.search(r"\d+", raw_date)
            raw_number = int(raw_date[rgx.span()[0]:rgx.span()[1]])
        except (ValueError, TypeError, AttributeError):
            print(raw_date)
            return DATE
        if 'minute' in raw_date:
            date = DATE - timedelta(minutes=raw_number)
        elif 'hour' in raw_date:
            date = DATE - timedelta(hours=raw_number)
        elif 'day' in raw_date or 'giorn' in raw_date or 'jour' in raw_date:
            date = DATE - timedelta(days=raw_number)
        elif 'week' in raw_date:
            date = DATE - timedelta(weeks=raw_number)
        elif 'month' in raw_date:
            date = DATE - timedelta(weeks=raw_number * 4)
        else:
            date = DATE
        return date


    def _create_entry(self, job_details, source, job_id, link):
        entry  = {
            'search_key': f'{self.job_title}&&{self.location}',
            'source': source,
            'job_id': job_id,
            'job_title': job_details['title'],
            'description': job_details['text'],
            'company': job_details['company'],
            'location': job_details['location'],
            'country': self.location,
            'date': job_details['date'],
            'link': link}
        return entry


class LinkedIn(Scraper):
    def __init__(self, cache, job_title, location):
        super().__init__(cache, job_title, location)
        self.parameters = {'keywords': job_title, 'location': location, 'start': 50}

        self.job_ids = self._get_ids()
        self.results = self._scrap_results()

    def _get_ids(self):
        job_ids = set()
        for start in range(0, 101, 25):
            url = f'https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords={self.job_title}&location={self.location}&start={start}'
            content = bs4_content(url)
            
            jobs = content.find_all('a', class_="result-card__full-card-link")
            for job in jobs:
                job_id = job.attrs['href'].split('/')[5].split('?')[0]
                job_ids.add(job_id)

        return job_ids

    def _fetch_details(self, content, job_details):
        job_details = super()._fetch_details(content, job_details)
        job_details['date'] = self.transform_date(job_details['date'])
        return job_details


    def _scrap_results(self):
        url = "https://www.linkedin.com/jobs/view/{job_id}/"
        count = 0
        for job_id in self.job_ids:
            if job_id not in self.cache:
                link = url.format(job_id=job_id)
                content = bs4_content(link)
                job_details = {
                    'title'   : {'tag': 'h3'     , 'class': 'sub-nav-cta__header'},
                    'company' : {'tag': 'a'      , 'class': 'topcard__org-name-link'},
                    'location': {'tag': 'span'   , 'class': 'topcard__flavor--bullet'},
                    'text'    : {'tag': 'section', 'class': 'description'},
                    'date'    : {'tag': 'span'   , 'class': 'posted-time-ago__text'}
                    }
                job_details = self._fetch_details(content, job_details)
                row = self._create_entry(job_details, 'LinkedIn', job_id, link)
                count += 1
                yield row

        print(f'added {count} offers from LinkedIn')


class Monster(Scraper):
    def __init__(self, links, cache, job_title, location):
        super().__init__(cache, job_title, location)
        self.extension = links[0]

        self.results_page_url = f"{links[1]}q={self.job_title}&page=10&geo=0"
        self.id_param = {
            'tag'  : 'a',
            'class': "view-details-link", 
            'attr' : 'href'}
        if links[1] != 'None': # If a country doesn't have monster
            self.job_ids = self._get_ids()
            self.results = self._scrap_results()
        
    def _fetch_details(self, content, job_details):        
        job_details = super()._fetch_details(content, job_details)
        raw_date = job_details['date']
        rgx = re.finditer(r"\d+", raw_date)
        try:
            rgx = [r for r in rgx][-1]
            beg = rgx.span()[0]
            end = rgx.span()[1]
            raw_date = raw_date[beg:end] + raw_date[end+1:end+8]
        except IndexError:
            raw_date = DATE

        job_details['date'] = self.transform_date(raw_date)
        return job_details

    def _scrap_results(self):
        count = 0
        for job_id in self.job_ids:
            if job_id not in self.cache:
                link = f"https://www.monster.{self.extension}{job_id}"
                content = bs4_content(link)

                job_details = {
                    'title'   : {'tag': 'h1' , 'class': 'job_title'},
                    'company' : {'tag': 'div', 'class': 'job_company_name tag-line'},
                    'location': {'tag': 'div', 'class': 'location'},
                    'text'    : {'tag': 'div', 'class': 'job-description'},
                    'date'    : {'tag': 'div', 'class': 'job-details-container'}
                    }
                job_details = self._fetch_details(content, job_details)
                row = self._create_entry(job_details, 'Monster', job_id, link)
                count += 1
                yield row

        print(f'added {count} offers from Monster')


class Indeed(Scraper):
    def __init__(self, links, cache, job_title, location):
        super().__init__(cache, job_title, location)

        self.link = links[2]

        self.results_page_url = f"https://{links[0]}.indeed.com/jobs?q={self.job_title}"
        self.id_param = {
            'tag'  : 'div',
            'class': 'job_scraper/obsearch-SerpJobCard', 
            'attr' : 'data-jk'}

        self.job_ids = self._get_ids()
        self.results = self._scrap_results()

    def _scrap_results(self):
        count = 0
        for start in range(0, 100, 10):

            for job_id in self.job_ids:
                if job_id not in self.cache:
                    link = f"{self.link}jk={job_id}&start={start}"
                    content = bs4_content(link)

                    job_details = {
                        'title': {'tag': 'div', 'class': 'jobsearch-JobInfoHeader-title-container'},
                        'info' : {'tag': 'div', 'class': 'jobsearch-JobInfoHeader-subtitle'},
                        'text' : {'tag': 'div', 'class': 'jobsearch-jobDescriptionText'}
                        }

                    job_details = self._fetch_details(content, job_details)
                    row = self._create_entry(job_details, 'Indeed', job_id, link)
                    count += 1
                    yield row

        print(f'added {count} offers from Indeed')

    def _fetch_details(self, content, job_details):
        job_details = super()._fetch_details(content, job_details)
        print(job_details)
        print(job_details['info'])
        return job_details


def selenium_content(url):
    options = Options()
    options.add_argument("--headless")
    options.add_argument("user-agent=Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:88.0) Gecko/20100101 Firefox/88.0")

    # PROXY = "http://52.151.15.4:80"
    # options.add_argument('--proxy-server=%s' % PROXY)

    driver = webdriver.Chrome(options=options)
    driver.get(url)
    time.sleep(8)
    html = driver.execute_script('return document.body.innerHTML;')
    content = BeautifulSoup(html, 'html.parser')
    driver.close()

    return content

def bs4_content(url):
    source = requests.get(url)
    content = BeautifulSoup(source.text, 'html.parser')
    return content

if __name__ == '__main__':
    text ='30+ giorni fa'
    rgx = re.finditer(r"\d+", text)
    rgx = [r for r in rgx][-1]
    print(l)
    beg = l.span()[0]
    end = l.span()[1]
    print(text[beg:end] + text[end+1:end+8])
    print(text[beg:end+8])
