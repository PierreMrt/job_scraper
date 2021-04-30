from bs4 import BeautifulSoup
import requests


URL = 'https://www.linkedin.com/jobs/search/?'


def scrap(db, job_title, location, days, table_name):
    """ Add Monster, glassdoor, ... scraping"""
    LinkedInScrap(db, job_title, location, days=days, table_name=table_name)


class LinkedInScrap:
    def __init__(self, db, job_title, location, days, table_name):

        self.parameters = {'f_TPR': f'r{days * 86400}', 'keywords': job_title, 'location': location, 'start': 0}

        self.db = db
        self.table = table_name

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

            row = (job_id, 'LinkedIn', title, description, company, location, '29/04/2021', link,)
            self.db.insert_into_table(self.table, row)
            self.db.conn.commit()

        print(f'Finished scraping with {error_count} errors.')
