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
        self.parameters = {'keywords': job_title, 'location': location, 'start': 50}

        self.db = db
        self.cache = cache

        self.location = location
        self.job_title = job_title

        self.job_ids = self._get_ids()
        self._scrap_results()

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
                    company = content.find('a', class_='topcard__org-name-link').text
                    location = content.find('span', class_='topcard__flavor--bullet').text
                    description = content.find('section', class_="description").text
                except AttributeError as e:
                    print(e)
                    continue

                row = (f'{self.job_title}&&{self.location}', 'LinkedIn', job_id, title, description, company, location, self.location,
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
    LinkedInScrap(None, [], 'data_analyst', 'france')