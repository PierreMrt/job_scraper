from job_search.scraping import scrap
from job_search.db_management import SqlConnexion

DB_NAME = 'jobs.db'


def get_active_search(db):
    actives = []
    db.curr.execute("SELECT search_key FROM search")
    searches = db.curr.fetchall()
    for search in searches:
        actives.append(search[0])

    return actives


def create_new_search(job_title, location):
    search_key = f'{job_title}&&{location}'

    db = SqlConnexion(DB_NAME)
    actives = get_active_search(db)
    print(actives)
    if search_key not in actives:
        row = ('pierre', job_title, location, search_key)
        db.curr.execute("INSERT INTO search values (NULL, ?, ?, ?, ?)", row)
        scrap(db, job_title, location)
    else:
        print(f'Search for {job_title} in {location} is already active.')

    df = db.db_to_panda(search_key)
    print(df)
    db.conn.close()


def update_searches():
    db = SqlConnexion(DB_NAME)
    actives = get_active_search(db)
    for search in actives:
        search_item = search.split('&&')
        scrap(db, search_item[0], search_item[1])

    db.conn.close()


if __name__ == '__main__':
    create_new_search('data_analyst', 'italy')
    # update_searches()
    db = SqlConnexion('jobs.db')
    sql = 'SELECT link FROM results'
    db.curr.execute(sql)
    links = db.curr.fetchall()
    [print(link) for link in links]

    # db = SqlConnexion('jobs.db')
    # tables = db.get_tables()
    # for table in tables:
    #     df = db.db_to_panda(table)
    #     print(df.head(20))



