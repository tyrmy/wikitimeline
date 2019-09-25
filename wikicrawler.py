#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# Ohjelma kerää wikipediasta henkilöhahmojen elinaikoja ja tallentaa ne tietokantaan.
# Tietokannan pohjalta on tehtävissä graafisia esityksiä datasta.

from datetime import date as d
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re

pages = set()

# Hakee infobox -nimisen html-kohteen wikipedia-sivulta. Ko. elementti sisältää henkilötietoja
def getInfobox(url):
    url = url.replace(' ', '_')
    try:
        html = urlopen('https://fi.wikipedia.org/wiki/'+url)
    except:
        print("Sivua ei löytynyt!")
        return
    bsObj = BeautifulSoup(html, 'lxml')
    try:
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

# Formatoi wikipedian suomenkielisen sivun päivämäärätiedon suomalaiseen numeeriseen muotoon
def convertDate(date):
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

# Hakee sivulta hotlinkkejä
def getLinks(pageUrl):
	global pages
	html = urlopen("http://en.wikipedia.org"+pageUrl)
	bsObj = BeautifulSoup(html)
	try:
		print(bsObj.h1.get_text())
		print(bsObj.find(id ="mw-content-text").findAll("p")[0].get_text())
		print(bsObj.find(id="ca-edit").find("span").find("a").attrs['href'])
	except AttributeError:
		print("This page is missing something! No worries though!")
	
	for link in bsObj.findAll("a", href=re.compile("^(/wiki/)")):
		if 'href' in link.attrs:
			if link.attrs['href'] not in pages:
				#We have encountered a new page
				newPage = link.attrs['href']
				print("----------------\n"+newPage)
				pages.add(newPage)
				getLinks(newPage)
#getLinks("/wiki/Kyra_Sedgwick")
getInfobox('Isaac Newton')
getInfobox('Urho Kekkonen')
getInfobox('Paavo Lipponen')
getInfobox('Mannerheim')
getInfobox('Prinsessa Diana')
getInfobox('John Kennedy')
getInfobox('George Boole')
getInfobox('Herodotos')
getInfobox('Aristoteles')
getInfobox('Platon')
getInfobox('Kolumbus')
getInfobox('Tarja Halonen')
getInfobox('Mick Jagger')
getInfobox('Ozzy Osbourne')
getInfobox('Frank Zappa')
getInfobox('Marco Hietala')
getInfobox('Tuomas Holopainen')
getInfobox('Timo Soini')
