from bs4 import BeautifulSoup
import requests
import re
from datetime import date

DATE = date.today().strftime("%d/%m/%Y")
URL = 'https://www.linkedin.com/jobs/search/?'


def scrap(db, job_title, location):
    """ Add Monster, glassdoor, ... scraping"""
    LinkedInScrap(db, job_title, location)
    IndeedScrap(db, job_title, location)


class LinkedInScrap:
    def __init__(self, db, job_title, location):

        self.parameters = {'keywords': job_title, 'location': location, 'start': 0}

        self.db = db
        self.location = location
        self.search_key = f"{job_title}&&{location}"

        self.job_ids = self._get_ids()
        self._scrap_results()

    def _bs4_content(self, start):
        self.parameters['start'] = start

        source = requests.get(URL, params=self.parameters)
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
        print(f"Getting {offers} jobs' ID in {pages} pages...")
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
        print(f"Scraping {len(self.job_ids)} job offers ...")

        error_count = 0
        for job_id in self.job_ids:
            link = url.format(job_id=job_id)
            source = requests.get(link)
            content = BeautifulSoup(source.text, 'html.parser')

            try:
                title = content.find('h3', class_="sub-nav-cta__header").text
                details = content.find('div', class_="sub-nav-cta__sub-text-container")
                company = details.find('a').text
                location = details.find('span').text
                description = content.find('section', class_="description").text
            except AttributeError:
                error_count += 1
                continue

            row = (self.search_key, 'LinkedIn', job_id, title, description, company, location, self.location,
                   DATE, link)
            self.db.insert_into_table(row)
            self.db.conn.commit()

        print(f'Finished scraping with {error_count} errors.')


class IndeedScrap:
    def __init__(self, db, job_title, location):
        self.db = db
        self.search_key = f"{job_title}&&{location}"
        self.location = location
        self.job_ids = self._get_ids()
        self._scrap_results()

    @staticmethod
    def _bs4_content(url):
        source = requests.get(url)
        content = BeautifulSoup(source.text, 'html.parser')
        return content

    def _get_ids(self):
        job_ids = []
        url = f"https://it.indeed.com/jobs?q=data_analyst"
        while not job_ids:
            content = self._bs4_content(url)
            jobs = content.find_all('div', class_="jobsearch-SerpJobCard")

            for job in jobs:
                job_ids.append(job.attrs['data-jk'])

        return job_ids

    def _scrap_results(self):
        for start in range(0, 100, 10):
            url = "https://it.indeed.com/offerta-lavoro?jk={job_id}&start={start}"
            print(f"Scraping {len(self.job_ids)} job offers ...")

            for job_id in self.job_ids:
                link = url.format(job_id=job_id, start=start)
                content = self._bs4_content(link)
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

                row = (self.search_key, 'Indeed', job_id, title, text, company, location, self.location,
                       DATE, link)
                self.db.insert_into_table(row)
                self.db.conn.commit()


class MonsterScrap:
    def __init__(self, db, job_title, location):
        self.db = db
        self.search_key = f"{job_title}&&{location}"
        self.job_title = job_title
        self.job_ids = self._get_ids()

    def _bs4_content(self, url):
        source = requests.get(url)
        content = BeautifulSoup(source.text, 'html.parser')
        return content

    def _get_ids(self):
        url = f"https://www.monster.it/lavoro/cerca?q=data+analyst"
        content = self._bs4_content(url)

        jobs = content.find_all('div')
        for job in jobs:
            print(job)


if __name__ == '__main__':
    scrap = IndeedScrap(None, 'data_analyst', 'italy')
    # print(scrap.job_ids)
    # print(len(scrap.job_ids))