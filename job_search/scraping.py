from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import requests
import re
from datetime import date

DATE = date.today().strftime("%d/%m/%Y")


class LinkedInScrap:
    def __init__(self, db, cache, job_title, location):

        self.parameters = {'keywords': job_title, 'location': location, 'start': 0}

        self.db = db
        self.cache = cache
        self.location = location
        self.search_key = f"{job_title}&&{location}"

        self.job_ids = self._get_ids()
        self._scrap_results()

    def _bs4_content(self, start):
        self.parameters['start'] = start
        url = 'https://www.linkedin.com/jobs/search/?'
        source = requests.get(url, params=self.parameters)
        content = BeautifulSoup(source.text, 'html.parser')
        return content

    def _nb_offers(self):
        content = self._bs4_content(start=0)
        nb_offers = content.find('span', class_="results-context-header__new-jobs").text
        nb_offers = int(''.join(c for c in nb_offers if c.isdigit()))
        return nb_offers

    def _get_ids(self):
        offers = self._nb_offers()
        pages = int(offers / 25)
        job_ids = set()
        for page in range(0, pages):
            content = self._bs4_content(start=page * 10)

            jobs = content.find('ul', class_="jobs-search__results-list")

            cards = jobs.find_all('li')
            for card in cards:
                job_id = card['data-id']
                job_ids.add(job_id)

        return job_ids

    def _scrap_results(self):
        url = "https://www.linkedin.com/jobs/view/{job_id}/"
        count = 0
        for job_id in self.job_ids:
            if job_id not in self.cache:
                link = url.format(job_id=job_id)
                source = requests.get(link)
                content = BeautifulSoup(source.text, 'html.parser')

                try:
                    title = content.find('h3', class_="sub-nav-cta__header").text
                    details = content.find('div', class_="sub-nav-cta__sub-text-container")
                    company = details.find('a').text
                    location = details.find('span').text
                    description = content.find('section', class_="description").text
                except AttributeError as e:
                    continue

                row = (self.search_key, 'LinkedIn', job_id, title, description, company, location, self.location,
                    DATE, link)
                self.db.insert_into_table(row)
                self.db.conn.commit()
                count += 1

        print(f'added {count} offers from LinkedIn')


class IndeedScrap:
    def __init__(self, db, links, cache, job_title, location):
        self.db = db
        self.cache = cache

        self.extension = links[0]
        self.link = links[2]

        self.job_title = job_title
        self.location = location

        self.job_ids = self._get_ids()
        self._scrap_results()

    def _get_ids(self):
        job_ids = []
        url = f"https://{self.extension}.indeed.com/jobs?q={self.job_title}"

        content = selenium_content(url)
        if content.find('div', class_='h-captcha') is not None:
            print('captcha')

        else:
            jobs = content.find_all('div', class_="jobsearch-SerpJobCard")

            for job in jobs:
                job_ids.append(job.attrs['data-jk'])

        return job_ids

    def _scrap_results(self):
        count = 0
        for start in range(0, 100, 10):

            for job_id in self.job_ids:
                if job_id not in self.cache:
                    url = f"{self.link}jk={job_id}&start={start}"
                    content = bs4_content(url)
                    title = content.find('div', class_='jobsearch-JobInfoHeader-title-container').text
                    info = content.find('div', class_='jobsearch-JobInfoHeader-subtitle').find_all('div')

                    company = info[0].text
                    company = re.split(r'(\d+)', company)[0]
                    if len(info) > 4:
                        location = info[8].text
                    else:
                        location = info[2].text
                    location = re.split(r'(\d+)', location)[-1]

                    text = content.find('div', class_='jobsearch-jobDescriptionText').text

                    row = (f'{self.job_title}&&{self.location}', 'Indeed', job_id, title, text, company, location, self.location,
                        DATE, url)
                    self.db.insert_into_table(row)
                    self.db.conn.commit()
                    count += 1

        print(f'added {count} offers from Indeed')


class MonsterScrap:
    def __init__(self, db, links, cache, job_title, location):
        self.db = db
        self.cache = cache

        self.extension = links[0]
        self.link = links[1]

        self.job_title = job_title
        self.location = location

        self.job_ids = self._get_ids()
        self._scrap_results()

    def _get_ids(self):
        job_ids = []
        url = f"{self.link}q={self.job_title}&page=10&geo=0"
        content = selenium_content(url)
        jobs = content.find_all('a', class_="view-details-link")
        for job in jobs:
            job_ids.append(job.attrs['href'])
        return job_ids

    def _scrap_results(self):
        count = 0

        for job_id in self.job_ids:
            if job_id not in self.cache:
                url = f"https://www.monster.{self.extension}{job_id}"
                content = bs4_content(url)
                title = content.find('h1', class_='job_title').text
                company = content.find('div', class_="job_company_name tag-line").text
                location = content.find('div', class_='location').text
                text = content.find('div', class_="job-description").text

                row = (f'{self.job_title}&&{self.location}', 'Monster', job_id, title, text, company, location, self.location,
                    DATE, url)
                self.db.insert_into_table(row)
                self.db.conn.commit()
                count += 1

        print(f'added {count} offers from Monster')

def selenium_content(url):
    options = Options()
    options.add_argument("--headless")
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
    scrap = MonsterScrap(None, 'data_analyst', 'italy')
    # print(scrap.job_ids)
    # print(len(scrap.job_ids))
