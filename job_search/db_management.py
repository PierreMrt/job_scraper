import sqlite3
from sqlite3 import Error
import pandas as pd

PATH = 'db/{name}'


class SqlConnexion:
    def __init__(self, name):
        self.name = name
        self.conn = self._create_connexion()
        self.curr = self.conn.cursor()

        self.fields = ('id', 'search_key', 'source', 'job_id', 'job_title', 'description', 'company', 'location',
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
        statement = "CREATE TABLE {0} {1}".format(table_name, self.fields)
        self.curr.execute(statement)

    def insert_into_table(self, row):
        statement = 'INSERT INTO results {0} VALUES (NULL, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'.format(self.fields)
        self.curr.execute(statement, row)

    def db_to_panda(self, search_key):
        statement = "SELECT * FROM results WHERE search_key='{0}'".format(search_key)
        query = pd.read_sql_query(statement, self.conn)
        df = pd.DataFrame(query, columns=self.fields)

        return df

    def get_tables(self):
        active_tables = []
        self.curr.execute("SELECT name FROM sqlite_master WHERE type = 'table'")
        tables = self.curr.fetchall()

        for table in tables:
            active_tables.append(table[0])

        return active_tables


def get_job_ids(db):
    db.curr.execute("SELECT job_id FROM results")
    job_ids = db.curr.fetchall()
    set_ids = set()

    for i in job_ids:
        set_ids.add(i[0])

    return set_ids


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


if __name__ == '__main__':
    db_name = 'jobs.db'
    create_database(db_name)
    create_tables(db_name)



