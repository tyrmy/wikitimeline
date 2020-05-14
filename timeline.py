# -*- coding: utf-8 -*-
"""
Created on 1 Jul 2019

@author Lassi Lehtinen
"""

import sqlite3
from sqlite3 import Error

import requests
from requests.exceptions import HTTPError, ConnectionError

from bs4 import BeautifulSoup
import re

import matplotlib.pyplot as plt
import matplotlib.dates as mdates

from time import sleep
from datetime import date as d
import datetime

from random import sample

db_loc = './data/wiki.db'
years = mdates.YearLocator(10)
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
        #sleep(1)
        dt = []
        try:
            url = fi_wiki_url(person)
            uri = get_url(url)
            if uri is None:
                print('store_list: due to connection error skipping...')
                print("--------------")
                continue
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
    """ Count days between two date objects. Returns int """
    return abs((d2 - d1).days)

def dict_factory(cursor, row):
    """ Makes a sqlite3 quary retrun a dictionary """
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

def get_url(url):
    """ Get page content as a string of html """
    print(url)
    try:
        html = requests.get(url, timeout=5, allow_redirects=True)
        print('success %r' % html)
    except (HTTPError, ConnectionError) as e:
        print("get_url: ", e)
        html = None
    return html.text

def fi_wiki_url(name):
    """ Create a finnish wikipedia page url from a persons name """
    name = name.replace(' ', '_')
    return 'https://fi.wikipedia.org/wiki/'+name

def en_wiki_url(name):
    """ Create an english wikipedia page url from a persons name """
    name = name.replace(' ', '_')
    return 'https://en.wikipedia.org/wiki/'+name

def print_persons(input_list):
    """ Try to find people based on a list of names. Prints results on the command line """
    for person in input_list:
        sleep(5)
        print_infobox(person)

def get_infobox(html):
    bsObj = BeautifulSoup(html, 'lxml')
    infobox = bsObj.find("table", {"class": "infobox"})
    if infobox is None:
        raise ValueError('get_infobox: Infobox not found!')
    else:
        print('get_infobox: infobox found!')
        return infobox

def dates(html):
    """ Primary way of finding dates. Takes the html """
    dates = []
    try:
        infobox = get_infobox(html)
    except ValueError as e:
        print('dates: ', e)
        return
    try:
        # Splits result at a keyword
        spot = infobox.get_text().split('Syntynyt')[1]
        for date in re.findall('[0-9]{1,2}\.\ [äöÄÖA-Za-z]{3,12}\ [0-9]{4}', spot):
            print('dates: "{}"'.format(date))
            newform = convertDate(date)
            print('dates: newform = {}'.format(newform))
            new = datetime.datetime.strptime(newform, '%d.%m.%Y').date()
            dates.append(new)
            if len(dates) == 2:
                break
        return dates
    except IndexError as e:
        print('dates: something went wrong when parsing dates from infobox...')
        print('dates: ', e)
        return

def dates_backup(html):
    """ Secondary way of finding dates. Takes raw html """
    dates = []
    bsObj = BeautifulSoup(html, 'lxml')
    paragraph = bsObj.find("div", {"id": "mw-content-text"})
    if paragraph is not None:
        for date in re.findall('[0-9]{1,2}\.\ [ÄÖäöA-Za-z].*?\ [0-9]{4}', paragraph.get_text()):
            print('dates_backup: '.format(date))
            try:
                newform = convertDate(date)
                print('dates_backup: newform = {}'.format(newform))
                new = datetime.datetime.strptime(newform, '%d.%m.%Y').date()
                dates.append(new)
                if len(dates) == 2:
                    break
            except:
                print("dates_backup: datetime format error")
        return dates
    if dates is not None:
        return dates
    else:
        print("dates_backup: no luck")

def print_by_age():
    """ Print people on command line sorted by total age """

    get = "SELECT * FROM people"
    try:
        con = sqlite3.connect(db_loc)
        con.row_factory = dict_factory
        cur = con.cursor()
        cur.execute(get)
    except Error as e:
        print("print_by_age: ", e)

    source = cur.fetchall()
    con.close()

    source = add_dates(source)
    for i in source:
        age = days_between(i['bday'],i['dday'])
        i['age'] = age

    print("{:<12} {:<12} {:<10}".format('Last name', 'First name', 'Age'))
    for life in sorted(source, key = lambda i: i['age']):
        year_format = to_years(life['age'])
        print("{:<12} {:<12} {:<10}".format(life['lname'], life['fname'], year_format))
        #print("{:<12} {:<12} {:<10}".format(life['lname'], life['fname'], life['age']))

def to_years(days):
    """ Convert days to approximate years and days """
    return "{} y {} d".format(int(days/365), days % 365)

def print_infobox(name):
    """ Fetch birthday and passing dates """
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

def plot_persons(amount):
    """ 
    Plots lifetime timelines from database to a matlib plot.
    Fetches all data from sqlite database and takes a random sample basen on param amount.
    """
    try:
        con = sqlite3.connect(db_loc)
        con.row_factory = dict_factory
        cur = con.cursor()
        #cur.execute("SELECT fname, lname, bday, dday FROM people WHERE bday LIKE \'19%\'")
        cur.execute("SELECT fname, lname, bday, dday FROM people")
    except Error as e:
        print("plot_persons: ", e)

    fig, ax = plt.subplots(figsize=(10,6))
    fig.tight_layout()

    index = 1
    source = cur.fetchall()
    con.close()
    
    people = sample(source, amount)
    people = add_dates(people)

    for life in sorted(people, key = lambda i: i['bday']):
        name = '{} {}'.format(life['fname'], life['lname'])
        plt.plot([life['bday'], life['dday']], [index, index], linewidth=4, label=name)
        index += 1

    plt.ylim(bottom=0, top=amount+1)
    plt.xlim(right=d.today())
    ax.legend()
    ax.xaxis.set_major_locator(years)
    ax.xaxis.set_minor_locator(years_minor)
    fig.autofmt_xdate()
    plt.gca().axes.get_yaxis().set_visible(False)
    #plt.tight_layout(pad=0.05, h_pad=0.2, w_pad=0.2)
    plt.grid(True)

    legend_col = int(len(people)/30)+1
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(handles[::-1], labels[::-1], title='Names', loc='upper left', fontsize='x-small', shadow=True, ncol=legend_col)
    plt.savefig('./images/timeline_02.png', dpi=100)
    plt.show()

def add_dates(input_dict):
    """ Change dict string dates to datetime objects """
    for person in input_dict:
        person['bday'] = datetime.datetime.strptime(person['bday'], '%Y-%m-%d').date()
        if ( person['dday'] == None ):
            person['dday'] = d.today()
        elif ( person['dday'] == 'None' ):
            person['dday'] = d.today()
        elif (isinstance(person['dday'], str)):
            person['dday'] = datetime.datetime.strptime(person['dday'], '%Y-%m-%d').date()
    return input_dict

def user_input():
    """ Interactive way of inputting people data to database """
    person = ''
    print("Input people to database:")
    while person is not 'quit':
        person = input('Name: ')
        if person == 'quit' or person == 'q':   
             break
        elif person == 'print' or person == 'p':
            count = input('How many:')
            plot_persons(int(count))
            continue
        elif person == 'age':
            print_by_age()
            continue
        store_list([person])
    print("Exiting...")

if __name__ == '__main__':
    user_input()
