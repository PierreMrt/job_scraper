import sqlite3
from sqlite3 import Error
import pandas as pd
from pathlib import Path

PATH = str(Path.cwd()) + '/job_search/db/{name}'


class SqlConnexion:
    def __init__(self, name):
        self.name = name
        self.conn = self._create_connexion()
        self.curr = self.conn.cursor()

        self.results_fields = ('id', 'search_key', 'source', 'job_id', 'job_title', 'description', 'company', 'location',
                       'country', 'date', 'link')

    def _create_connexion(self):
        path = PATH.format(name=self.name)

        conn = None
        try:
            conn = sqlite3.connect(path)
            print(f'connected to {self.name}')
        except Error as e:
            print(e)

        return conn

    def create_table(self, table_name):
        statement = "CREATE TABLE {0} {1}".format(table_name, self.results_fields)
        self.curr.execute(statement)

    def db_to_panda(self, search_key):
        statement = "SELECT * FROM results WHERE search_key='{0}'".format(search_key)
        query = pd.read_sql_query(statement, self.conn)
        df = pd.DataFrame(query, columns=self.results_fields)

        return df

    def get_tables(self):
        active_tables = []
        self.curr.execute("SELECT name FROM sqlite_master WHERE type = 'table'")
        tables = self.curr.fetchall()

        for table in tables:
            active_tables.append(table[0])

        return active_tables


def create_database(name):
    path = PATH.format(name=name)

    conn = None
    try:
        conn = sqlite3.connect(path)
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()


def create_tables(db_name):
    db = SqlConnexion(db_name)
    conn = db.conn
    c = conn.cursor()

    # create search table
    sql = """CREATE TABLE IF NOT EXISTS search (
                id integer PRIMARY KEY,
                user text NOT NULL,
                job text,
                country text,
                search_key text
            )"""
    c.execute(sql)

    # create links table
    sql = """CREATE TABLE IF NOT EXISTS links (
                id integer PRIMARY KEY,
                country text NOT NULL,
                extension text,
                LinkedIn text,
                Monster text,
                Indeed text
            )"""
    c.execute(sql)

    # create users table
    sql = """CREATE TABLE IF NOT EXISTS users (
                id integer PRIMARY KEY,
                username text NOT NULL,
                mail text,
                password text
            )"""
    c.execute(sql)
    # create results table
    sql = """CREATE TABLE IF NOT EXISTS results (
                id integer PRIMARY KEY,
                search_key text NOT NULL,
                source text,
                job_id,
                job_title text,
                description text,
                company text,
                location text,
                country text,
                date datetime,
                link text       
            )"""
    c.execute(sql)

    conn.close()

def populate_links_table(db_name):
    db = SqlConnexion(db_name)
    links = [(None, 'italy', 'it', 'www.linkedin.com', 'https://www.monster.it/lavoro/cerca?', 'https://it.indeed.com/offerta-lavoro?'),
             (None, 'france', 'fr', 'www.linkedin.com', 'https://www.monster.fr/emploi/recherche?', 'https://fr.indeed.com/voir-emploi?'),
             (None, 'uruguay', 'uy', 'www.linkedin.com', None, 'https://uy.indeed.com/descripción-del-puesto?'),
             (None, 'austria', 'at', 'www.linkedin.com', 'https://www.monster.at/jobs/suche?', 'https://at.indeed.com/Zeige-Job?')
    ]
    db.curr.executemany('INSERT INTO links VALUES(?, ?, ?, ?, ?, ?);', links)
    print(f'{db.curr.rowcount} rows inserted')
    db.conn.commit()
    db.conn.close()

if __name__ == '__main__':
    db_name = 'jobs.db'
    # create_database(db_name)
    # create_tables(db_name)
    populate_links_table(db_name)



