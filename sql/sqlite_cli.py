"""
Created on Mar 10, 2020

@author: Lassi Lehtinen
A basic sqlite3-Python interface. Includes printing options for CLI.
"""

import os
from sqlite_base import sql_base as base
from sqlite3 import Error

from prettytable import PrettyTable
from prettytable import from_db_cursor

from time import sleep
from datetime import datetime

class sqlite_cli(base):
    def run(self):
        #for i in range(1,10):
        while True:
            self.get_state()
            print("--------\n")
            print("{}".format(datetime.now()))
            sleep(10)

    def get_state(self):
        os.system('clear')
        self.get_table_names()
        self.get_table_columns()
        self.count_values()
        self.print_latest()

    def count_values(self):
        """ Returns the count of values in a table specified """
        for table in self.tables:
            try:
                self.cur.execute('SELECT COUNT(*) FROM {}'.format(table))
                total = self.cur.fetchone()[0]
                print("{}: {}".format(table, total))
            except Error as e:
                print("count_values: {}".format(e))
        print('--------')

    def print_latest(self):
        """ Prints 10 latest rows of every column in database using PrettyTable """
        for table in self.tables:
            try:
                print(table.upper())
                self.cur.execute('SELECT * FROM {} ORDER BY id DESC LIMIT 5'.format(table))
                t = from_db_cursor(self.cur)
                print(t)
            except Error as e:
                print("print_latest: {}".format(e))

    def get_table_columns(self):
        """ Prints the columns names of a table specified """
        for table in self.tables:
            try:
                self.cur.execute("SELECT * FROM " + table)
                rows = [description[0] for description in self.cur.description]
                print((table + ": ").upper(), end='')
                for name in rows:
                    print(name, end=', ')
                print('')
            except Error as e:
                print("get_table_columns: {}".format(e))
        print('--------')

    def get_table_names(self):
        """ Print database table names """
        try:
            self.cur.execute("select name from sqlite_master where type = \'table\'")
            rows = self.cur.fetchall()
            self.tables.clear()
            for i in rows:
                self.tables.append(i[0])
        except Error as e:
            print("get_table_names: ", e)

    def print_all_from_table(self, table_name):
        """ Prints all rows of every column in database using PrettyTable """
        try:
            self.cur.execute('SELECT * FROM {}'.format(table_name))
            t = from_db_cursor(self.cur)
            print(t)
        except Error as e:
            print("print_all_from_table: {}".format(e))

if __name__ == '__main__':
    sq = sqlite_cli()
    sq.connect('./databases/wiki')
    try:
        sq.run()
    except KeyboardInterrupt:
        print('Exiting...')
    sq.close()
