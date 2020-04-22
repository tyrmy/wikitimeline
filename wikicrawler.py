"""
Created on 1.7.2019

@author Lassi Lehtinen
"""
from datetime import date as d
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re

import matplotlib.pyplot as plt
import matplotlib.dates as mdates

dates = [[d(1995,3,15),d.today()],
        [d(1993,4,23),d.today()],
        [d(1968,3,2),d.today()],
        [d(1969,2,13),d.today()]]

names = ['Lassi Lehtinen', 'Matilda Lintunen', 'Hannu Lehtinen', 'Tarja Salminen']

years = mdates.YearLocator(5)
years_minor = mdates.YearLocator(1)
persons = ['Urho Kekkonen', 'Paavo Lipponen', 'Mannerheim', 'Prinsessa Diana', 'John Kennedy', 'Tarja Halonen', 'Mick Jagger', 'Ozzy Osbourne', 'Frank Zappa', 'Marco Hietala', 'Tuomas Holopainen', 'Timo Soini', 'Alan Turing', 'Ben Stiller', 'Conan O\'Brian', 'Arnold Schwarzenegger']
pages = set()

def printInfobox(url):
    """ Fetch information from infobox element """
    url = url.replace(' ', '_')
    try:
        html = urlopen('https://fi.wikipedia.org/wiki/'+url)
    except:
        print("Sivua ei löytynyt!")
        return
    try:
        bsObj = BeautifulSoup(html, 'lxml')
        infobox = bsObj.find("table", {"class": "infobox"})
        print(bsObj.h1.get_text())
        for date in re.findall('[0-9]{1,2}\.\ [A-Za-z].*\ [0-9]{4}', infobox.get_text().split('Syntynyt')[1]):
            fix = convertDate(date)
            new = d(fix[2],fix[1],fix[0])	
            print(new.strftime("%d.%m.%Y"))
    except:
        print("Syntymätietoja ei löytynyt! Etsitään leipätekstistä...")
        paragraph = bsObj.find("div", {"id": "mw-content-text"})
#        print(paragraph.get_text())
        if paragraph is not None:
            for date in re.findall('[0-9]{1,2}\.\ [A-Za-z].*?\ [0-9]{4}', paragraph.get_text()):
                #print(date)
                try:
                    fix = convertDate(date)
                    new = d(fix[2],fix[1],fix[0])	
                    print(new.strftime("%d.%m.%Y"))
                except:
                    print("Kelvoton pvm...")
        else:
            print("Ei löytynyt...")
    print("--------")
    return

def getLifecycle(name):
    """ Fetch information from infobox element and return a list """
    name = name.replace(' ', '_')
    dates = []
    try:
        html = urlopen('https://fi.wikipedia.org/wiki/'+name)
    except:
        print("Error: Can't find page")
        return []
    try:
        bsObj = BeautifulSoup(html, 'lxml')
        infobox = bsObj.find("table", {"class": "infobox"})
        for date in re.findall('[0-9]{1,2}\.\ [A-Za-z].*\ [0-9]{4}', infobox.get_text().split('Syntynyt')[1]):
            fix = convertDate(date)
            new = d(fix[2],fix[1],fix[0])	
            dates.append(new)
        if len(dates) <= 1:
            dates.append(d.today())
        print(dates)
        return dates
    except:
        print("Syntymätietoja ei löytynyt! Etsitään leipätekstistä...")
        paragraph = bsObj.find("div", {"id": "mw-content-text"})
        if paragraph is not None:
            for date in re.findall('[0-9]{1,2}\.\ [A-Za-z].*?\ [0-9]{4}', paragraph.get_text()):
                try:
                    fix = convertDate(date)
                    new = d(fix[2],fix[1],fix[0])	
                    print(new.strftime("%d.%m.%Y"))
                    dates.append(new)
                except:
                    print("Kelvoton pvm...")
                if len(dates) <= 1:
                    dates.append(d.today())
                print(dates)
                return dates
        else:
            print("Ei löytynyt...")
    print("--------")
    return

def convertDate(date):
    """ Formatoi wikipedian suomenkielisen sivun päivämäärätiedon suomalaiseen numeeriseen muotoon """
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

    newdate = newdate.split('.')
    intlist = []
    for i in newdate:
        intlist.append(int(i))
    return intlist

if __name__ == '__main__':
    for person in persons:
        dates.append(getLifecycle(person))
        names.append(person)

    fig,ax = plt.subplots(1)

    index = [1,1]
    name_index = 0
    for life in dates:
         plt.plot(life, index, linewidth=4, label=names[name_index])
         index = [i+1 for i in index]
         name_index += 1
    plt.ylim(bottom=0, top=len(dates)+1)
    ax.legend()
    ax.xaxis.set_major_locator(years)
    ax.xaxis.set_minor_locator(years_minor)
    fig.autofmt_xdate()
    plt.gca().axes.get_yaxis().set_visible(False)
    plt.tight_layout(.5)
    plt.grid(True)
    plt.show()
