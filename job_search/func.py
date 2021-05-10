from scraping import LinkedIn, Indeed, Monster
from db_management import SqlConnexion

DB_NAME = 'jobs.db'


def scrap(db, job_title, location):
    links = get_links(db, location)
    cache = cached_ids(db)
    LinkedIn(db, cache, job_title, location)
    Indeed(db, links, cache, job_title, location)
    Monster(db, links, cache, job_title, location)


def get_links(db, country):
    sql = 'SELECT extension, Monster, Indeed FROM links WHERE country=?'
    sql = db.curr.execute(sql, (country,))
    results = db.curr.fetchall()
    return results[0]

def cached_ids(db):
    cached_ids = set()
    db.curr.execute("SELECT job_id FROM results")
    cache = db.curr.fetchall()
    [cached_ids.add(i[0]) for i in cache]

    return cached_ids

def get_active_search(db):
    actives = []
    db.curr.execute("SELECT search_key FROM search")
    searches = db.curr.fetchall()
    for search in searches:
        actives.append(search[0])

    return actives


def create_new_search(job_title, location):
    job_title = job_title.lower()
    locaton = location.lower()

    search_key = f'{job_title}&&{location}'

    db = SqlConnexion(DB_NAME)
    actives = get_active_search(db)
    if search_key not in actives:
        row = ('pierre', job_title, location, search_key)
        db.curr.execute("INSERT INTO search values (NULL, ?, ?, ?, ?)", row)
        scrap(db, job_title, location)
    else:
        print(f'Search for {job_title} in {location} is already active.')

    # df = db.db_to_panda(search_key)
    # print(df)
    db.conn.close()


def update_searches():
    db = SqlConnexion(DB_NAME)
    actives = get_active_search(db)
    for search in actives:
        search_item = search.split('&&')
        print(f'Scraping offers for {search_item[0]} in {search_item[1]}')
        scrap(db, search_item[0], search_item[1])

    db.conn.close()

def delete_search(search_key):
    db = SqlConnexion(DB_NAME)
    sql = 'DELETE FROM results WHERE search_key=?'
    db.curr.execute(sql, (search_key,))
    sql = 'DELETE FROM search WHERE search_key=?'
    db.curr.execute(sql, (search_key,))

    db.conn.commit()
    db.conn.close()