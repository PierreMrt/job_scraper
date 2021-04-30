import sqlite3
from sqlite3 import Error
import pandas as pd

PATH = 'db/{name}'


class SqlConnexion:
    def __init__(self, name):
        self.name = name
        self.conn = self._create_connexion()
        self.curr = self.conn.cursor()

        self.fields = ('ID', 'source', 'title', 'text', 'country', 'city', 'date', 'link')

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

    def insert_into_table(self, table, row):
        statement = 'INSERT INTO "{0}" {1} VALUES (?, ?, ?, ?, ?, ?, ?, ?)'.format(table, self.fields)
        self.curr.execute(statement, row)

    def db_to_panda(self, table):
        statement = "SELECT * FROM {0}".format(table)
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


if __name__ == '__main__':
    create_database('jobs.db')


