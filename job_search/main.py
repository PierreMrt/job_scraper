from scraping import scrap
from db_management import SqlConnexion

DB_NAME = 'jobs.db'


def create_new_search(job_title, location):
    table_name = f'{job_title}in{location}'

    db = SqlConnexion(DB_NAME)

    if table_name not in db.get_tables():
        db.create_table(table_name)
        scrap(db, job_title, location, days=10, table_name=table_name)
    else:
        print(f'Search for {job_title} in {location} is already active.')

    df = db.db_to_panda(table_name)
    print(df)
    db.conn.close()


def update_searches():
    db = SqlConnexion(DB_NAME)
    active_search = db.get_tables()
    for search in active_search:
        search_item = search.split('in')
        scrap(db, search_item[0], search_item[1], days=1, table_name=search)

    db.conn.close()


if __name__ == '__main__':
    create_new_search('data analyst', 'France')
    # update_searches()

    # db = SqlConnexion('jobs.db')
    # tables = db.get_tables()
    # for table in tables:
    #     df = db.db_to_panda(table)
    #     print(df.head(20))



