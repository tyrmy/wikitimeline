"""
Created on May 3, 2020

@author: Lassi Lehtinen
sqlite3-Python interface base class
"""

import sqlite3
import os
from sqlite3 import Error

db_loc = './databases/wiki.db'

class sql_base():
    def __init__(self):
        """ Contructs a new sqlite object. Takes no arguments. """
        self.con = None
        self.cur = None
        self.tables = []
        self.current_database = 'not connected'

    def __str__(self):
        """ String method """
        return 'sql_object:\n{}\n{}'.format(self.current_database, self.tables)

    def execute_sql(self, location):
        """ Executes the sql quary specified """
        try:
            with open(location, 'rb') as sql_script:
                self.cur.executescript(sql_script)
        except Error as e:
            print("execute_sql: {}".format(e))

    def connect(self, db_file):
        """ Enstablish a connection to a database file """
        self.current_database = db_file
        try:
            self.con = sqlite3.connect(db_file)
            self.con.row_factory = sqlite3.Row
            print("Successful connection to {}!".format(db_file))
            print("SQLite version: " + sqlite3.version)
            self.cur = self.con.cursor()
        except Error as e:
            print("create_connection: {}".format(e))

    def close(self):
        """ Closes the connection safely """
        if self.con:
            try:
                self.con.close()
            except Error as e:
                print("close connection: {}".format(e))
            else:
                print("Connection closed!")

    def update(self, update):
        """ Optional function for updating local database with an external command """
        os.system(update)

if __name__ == '__main__':
    sq = sql_base()
    sq.connect(db_loc)
    sq.close()
