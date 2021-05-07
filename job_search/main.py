from scraping import scrap
from db_management import SqlConnexion

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

if __name__ == '__main__':
    delete_search('data_analyst&&france')
    create_new_search('data_analyst', 'france')
    # update_searches()
    # db = SqlConnexion('jobs.db')
    # sql = 'SELECT link FROM results'
    # db.curr.execute(sql)
    # links = db.curr.fetchall()
    # [print(link) for link in links]





