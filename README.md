# Job Scraper
job scraper is a web app that allow you to set up job searches via the scraping of different platforms (linkedin, monster...).

## :bulb: What is the idea behind this project?

All jobs offers in the same place. Advanced filters to find the perfect job.



## :open_book: How can I contribute ?

At the bottom of this file, you'll find a task list to easily view where the project stands at.

If you are a contributor and you want to start adding some code follow this procedure (this is using the CLI/Terminal/Command Interface):
The following steps will assume that you are using the Windows Command Line.

1. Clone the repository

> Navigate to the folder in which you want to store this project then write `git clone https://github.com/PierreMrt/job_scraper.git`. To enter the created folder, use `cd job_scraper`.

2. Create a pip environment with virtualenv

> Because we are using python and to assure compatibility between contributors, we use virtualenv. First, check that virtualenv is installed by writing `virtualenv` in your command line. If it doesn't recognise it, simply install it with `pip install virtualenv`. Then create your environement with `virtualenv env_VERSION_OF_PYTHON`. Replace VERSION_OF_PYTHON with your current Python version. Check it with `py --version`.

3. Enter the pip environment with virtualenv

> To use it, enter the following line in your terminal `env_VERSION_OF_PYTHON\Scripts\activate`. You should see (env_3_9_2) at the left of the current folder position `(env_VERSION_OF_PYTHON) C:\Users\JohnDoe\code\job_scrapper>`.

4. Install all pip dependencies

> If you check what files are currently sitting in the repo, you'll find `requirements.txt`. This files tells pip what dependencies to install with a version attached to it. To install all dependencies simply write `pip install -r requirements.txt`.

---

> I need to install a python library, how do it do it?

First, check that you are under the project's pip environment (in the terminal, you should have (env_3_9_2) at the left of your current foler position). Then, just run `pip install <your-library>`. It should be installed for the whole project. To know which version of the package you have write `pip freeze` and copy/paste the returned result in `requirements.txt`.

## :white_check_mark: Task list


- [x] get job offer publication's date
- [x] find a place for update button
- [x] offer language detection
- [x] dinamic filtering for views - advanced search
- [x] rename and clean repo
- [x] create account creation
- [x] create link with user
- [ ] manage captcha for indeed

## docs:
models: https://docs.djangoproject.com/en/3.2/topics/db/models/

MVC django: [https://overiq.com/django-1-10/mvc-pattern-and-django/

Celery: https://docs.celeryproject.org/en/latest/django/first-steps-with-django.html


## Help for setting up the database

Working with models sometimes means deleting `migrations` files and also deleting the `db.sqlite3` file.
There is an easy way to `populate` the database once your made the migrations, just follow these steps:

1. Delete all migration files in the migrations folder
2. Delete the db.sqlite3 file
3. Run `python manage.py makemigrations` then run ``python manage.py migrate jobs && python manage.py loaddata mydata.json`.

This will populate the database with some Links, Searches and Results.

You will also need to create a new user: `python manage.py createsuperuser`. This will prompt some questions regarding the credentials of that super user.

## Screenshots

* main page

![search_list](https://user-images.githubusercontent.com/69766734/120372171-19d53780-c317-11eb-9b3d-db91fd7812b3.png)

* Result list

![results_list](https://user-images.githubusercontent.com/69766734/120371868-b8ad6400-c316-11eb-80b2-b72cefdf27a7.png)

* Creating a new search

![new_search](https://user-images.githubusercontent.com/69766734/120371849-b21eec80-c316-11eb-9ac8-a5eb477a344b.png)