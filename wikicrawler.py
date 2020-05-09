# -*- coding: utf-8 -*-

"""
Created on 1 Jul 2019

@author Lassi Lehtinen
"""


import sqlite3
from sqlite3 import Error

from urllib.request import urlopen
from urllib.error import URLError

from bs4 import BeautifulSoup
import re

import matplotlib.pyplot as plt
import matplotlib.dates as mdates

from time import sleep
from datetime import date as d
import datetime

from random import sample

db_loc = './data/wiki.db'
years = mdates.YearLocator(5)
years_minor = mdates.YearLocator(1)

def store(name, born=None, died=None, source=None):
    """ Store a value to project specified database with columns mentioned below """
    names = name.split()
    store = """
        insert into people (fname, lname, bday, dday, source)
        values ('{fn}', '{ln}', '{bd}', '{dd}', '{s}')
    """.format(fn=names[0], ln=names[1], bd=born, dd=died, s=source)
    try:
        con = sqlite3.connect(db_loc)
        cur = con.cursor()
        cur.execute(store)
        con.commit()
        con.close()
    except Error as e:
        print("store: ", e)

def store_list(source):
    """ Start fetching dates from wikipedia with a list on names as input. Takes care of storing. """
    for person in source:
        sleep(5)
        dt = []
        try:
            url = fi_wiki_url(person)
            uri = get_url(url)
            if uri is None:
                print('store_list: due to connection error skipping...')
                print("--------------")
                continue
            print("Status code: ", uri.status)
            dt = dates(uri)
            print(dt)

            if len(dt) == 1:
                store(person, dt[0], source=url)
            elif len(dt) == 2:
                store(person, dt[0], dt[1], url)
            elif len(dt) == 0:
                print("store_list: len(dt) == 0")
            else:
                print("store_list: len(dt) > 2")
        except TypeError as e:
            print("store_list: ",e)
        print("--------------")

def days_between(d1, d2):
    """ Count days between two date objects """
    return abs((d2 - d1).days)

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

def get_url(url):
    """ Get page content """
    print(url)
    try:
        html = urlopen(url, timeout = 10)
    except URLError as e:
        print("get_url: ", e)
        html = None
    return html

def fi_wiki_url(name):
    """ Attach finnish wikipedia url """
    name = name.replace(' ', '_')
    return 'https://fi.wikipedia.org/wiki/'+name

def en_wiki_url(name):
    """ Attach english wikipedia url """
    name = name.replace(' ', '_')
    return 'https://en.wikipedia.org/wiki/'+name

def print_persons(input_list):
    """ Print information on command line """
    for person in input_list:
        sleep(5)
        print_infobox(person)

def dates(html):
    """ Primary way of finding dates """
    dates = []
    bsObj = BeautifulSoup(html, 'lxml')
    infobox = bsObj.find("table", {"class": "infobox"})
    if infobox is not None:
        for date in re.findall('[0-9]{1,2}\.\ [A-Za-z].*\ [0-9]{4}', infobox.get_text().split('Syntynyt')[1]):
            newform = convertDate(date)
            fix = datestr2numlist(newform)
            new = d(fix[2],fix[1],fix[0])	
            dates.append(new)
        return dates
    else:
        print('dates: infobox not found')

def dates_backup(html):
    """ Secondary way of finding dates """
    dates = []
    bsObj = BeautifulSoup(html, 'lxml')
    paragraph = bsObj.find("div", {"id": "mw-content-text"})
    if paragraph is not None:
        for date in re.findall('[0-9]{1,2}\.\ [A-Za-z].*?\ [0-9]{4}', paragraph.get_text()):
            try:
                newform = convertDate(date)
                fix = datestr2numlist(newform)
                new = d(fix[2],fix[1],fix[0])	
                dates.append(new)
            except:
                print("Kelvoton pvm...")
        return dates
    else:
        return None

def print_infobox(name):
    """ Fetch information from infobox element """
    print(name.upper())
    html = get_url(fi_wiki_url(name))
    if html is not None:
        try:
            dt = dates(html)
            if len(dt) == 1:
                dt.append(d.today())
            print(dt)
            age = days_between(dt[0],dt[1])
            print("{} days: {} years and {} days".format(age, int(age/365), age % 365))
        except:
            dt = dates_backup(html)
            if dt is not None:
                print(dt)
                age = days_between(dt[0],dt[1])
                print("{} days: {} years and {} days".format(age, int(age/365), age % 365))
            else:
                print("Nothing found...")
    print("--------")

def convertDate(date):
    """ Format finnish month names to numbers """
    newdate = re.sub('tammikuuta','1.', date)
    newdate = re.sub('helmikuuta','2.', newdate)
    newdate = re.sub('maaliskuuta','3.', newdate)
    newdate = re.sub('huhtikuuta','4.', newdate)
    newdate = re.sub('toukokuuta','5.', newdate)
    newdate = re.sub('kesäkuuta','6.', newdate)
    newdate = re.sub('heinäkuuta','7.', newdate)
    newdate = re.sub('elokuuta','8.', newdate)
    newdate = re.sub('syyskuuta','9.', newdate)
    newdate = re.sub('lokakuuta','10.', newdate)
    newdate = re.sub('marraskuuta','11.', newdate)
    newdate = re.sub('joulukuuta','12.', newdate)
    newdate = re.sub('\ ', '', newdate)
    return newdate

def datestr2numlist(date):
    """ Takes a date in string format and separated them to int list  """
    newdate = date.split('.')
    intlist = []
    for i in newdate:
        intlist.append(int(i))
    return intlist

def plot_persons(amount):
    """ Plots timelines from database TO BE MOVED"""
    try:
        con = sqlite3.connect(db_loc)
        con.row_factory = dict_factory
        cur = con.cursor()
        cur.execute("SELECT fname, lname, bday, dday FROM people")
    except Error as e:
        print("plot_persons: ", e)

    fig, ax = plt.subplots(1)

    index = 1
    source = cur.fetchall()
    people = sample(source, amount)

    for person in people:
        person['bday'] = datetime.datetime.strptime(person['bday'], '%Y-%m-%d').date()
        if ( person['dday'] == None ):
            person['dday'] = d.today()
        elif ( person['dday'] == 'None' ):
            person['dday'] = d.today()
        elif (isinstance(person['dday'], str)):
            person['dday'] = datetime.datetime.strptime(person['dday'], '%Y-%m-%d').date()

    for life in people:
        name = '{} {}'.format(life['fname'], life['lname'])
        plt.plot([life['bday'], life['dday']], [index, index], linewidth=4, label=name)
        index += 1

    plt.ylim(bottom=0, top=amount+1)
    ax.legend()
    ax.xaxis.set_major_locator(years)
    ax.xaxis.set_minor_locator(years_minor)
    fig.autofmt_xdate()
    plt.gca().axes.get_yaxis().set_visible(False)
    plt.tight_layout(pad=0.5, h_pad=0.5, w_pad=0.5)
    plt.grid(True)
    plt.show()
    con.close()

def user_input():
    person = ''
    print("Input people to database:")
    while person is not 'quit':
        person = input('Name: ')
        if person == 'quit':   
             break
        store_list([person])
    print("Exiting...")

if __name__ == '__main__':
    #print_persons(sample(randoms, 5))
    plot_persons(20)
    #store_list(sample(randoms, 20))
    #finnish = ['Aku Hirviniemi', 'Jaakko Saariluoma', 'Jonne Aaron', 'Mauno Koivisto', 'Urho Kekkonen', 'Risto Ryti', 'Tuomas Holopainen', 'Jenni Vartiainen']
    #store_list(finnish)
    #user_input()
