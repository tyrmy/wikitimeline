# Timeline

## Overview

Application for visualising peoples lifespans with _matplotlib_. Currently uses wikipedia as main source.

timeline.py contains all main functions. _requests_ library is used to fetch html pages from sources. _BeautifulSoup_ parses dates from wikipedias "infobox" element. The results and persons name are stored in a sqlite database.

Plotting is done bases on sql quaries.

## TBI

* Manual input

## Images

![timeline1](./images/timeline_01.png)
