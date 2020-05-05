"""
Created on Mar 10, 2020

@author: Lassi Lehtinen
Class for writing values to database
"""

from time import sleep
from sql.sqlite_base import sql_base as base

class sqlite_writer(base):
    def get_two_values(self, table, x, y):
        """ Get two values as lists for plotting etc """
        try:
            self.cur.execute('SELECT {value1},{value2} FROM {source} LIMIT 10'.format(value1=x, value2=y, source=table))
            rows = self.cur.fetchall()

            x = []
            y = []
            for row in rows:
                x.append(row[0])
                y.append(row[1])
            return x, y
        except Error as e:
            print("get_two_values: {}".format(e))

    def return_quary(self, input_string):
        """ Returns a list of rows given by sql quary """
        item_list = []
        try:
            self.cur.execute(input_string)
            for item in self.cur.fetchall():
                item_list.append(item)
            return item_list
        except Error as e:
            print("return_quary: {}".format(e))
            return 0

    def write_to_database(self, input_string):
        """ Executes an SQL quary to store values to database """
        try:
            self.cur.execute(input_string)
            self.con.commit()
            print("Values added to database!")
        except Error as e:
            print("write_to_database: ", e)
