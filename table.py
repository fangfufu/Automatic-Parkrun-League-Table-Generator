#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Parkrun Result Table Downloader
This is a part of Automatic Parkrun League Table Generator
Dedicated to UEA Triathlon Club
"""

import requests
from bs4 import BeautifulSoup
from util import sec_to_timestr, timestr_to_sec
from datetime import date

class HTTPError(Exception):
    pass

class TableNotFound(Exception):
    pass

class ParkrunEntry:
    def __init__(self, loc, eid, date, entry):
        self.pos = int(entry[0])
        self.name = entry[1]
        self.time = timestr_to_sec(entry[2])
        self.age_cat = entry[3]
        self.age_grade = float(entry[4].split(' ')[0])
        self.gender = entry[5]
        self.gender_pos = int(entry[6])
        self.club = entry[7]
        self.note = entry[8]
        self.total = entry[9]
        self.PB = False
        if self.note.find("New") != -1 or self.note.find("First") != -1:
            self.PB = True
        self.loc = loc
        self.eid = eid
        self.date = date

    def __repr__(self):
        txt = "|" + self.loc + ", " + str(self.eid) + ", " + str(self.pos)
        txt += ", " + self.name + ", " + sec_to_timestr(self.time) + ", "
        txt += str(self.age_grade) + "%, " + self.gender + ": "
        txt += str(self.gender_pos) + ", " + self.club + ", PB: "
        txt += str(self.PB) + "|"
        return txt

class ParkrunTable:
    '''
    The results from a single Parkriun for the selected clubs

    Args:
        loc(str): location of the Parkrun
        club_names(tuple): the name of the club
        eid(int): the Parkrun even number

    Attributes:
        tbl (list): List of Parkrun result entries.
    '''
    def __init__(self, loc, club_names, eid):
        def get_URL_content(url):
            """Get the content of a URL."""
            # Custom user-agent because Parkrun doesn't like webscraping.
            # (We are being naughty)
            custom_headers = {
                "User-Agent" : ("Mozilla/5.0 (X11; Linux x86_64) "
                            "AppleWebKit/537.36 (KHTML, like Gecko) "
                            "Chrome/74.0.3729.169 Safari/537.36")}
            r = requests.get(url, headers=custom_headers)

            if r.status_code != 200:
                raise HTTPError("Http Error, status code: " +
                                    str(r.status_code))
            return r.text

        def soup_to_tbl(loc, eid, date, soup):
            def html_tbl_to_list_tbl(html_tbl):
                list_tbl = []
                for html_row in html_tbl.findAll('tr'):
                    html_col = html_row.findAll('td')
                    row = []
                    for column in html_col:
                        row.append(column.text)
                    list_tbl.append(row)
                return list_tbl

            def filter_by_club(tbl_row):
                # Club name is always at the 8th column
                club = 7
                if not tbl_row:
                    return False
                if tbl_row[club] in club_names:
                    return True
                else:
                    return False

            html_tbl = soup.find(id="results")
            if html_tbl == None:
                raise TableNotFound("Result table not found!")

            list_tbl = html_tbl_to_list_tbl(html_tbl)
            filtered_tbl = list(filter(filter_by_club, list_tbl))

            entries = []
            for i in filtered_tbl:
                entries.append(ParkrunEntry(loc, eid, date, i))
            return entries

        # Generate the URL
        if str(eid) != "latest":
            url = "https://www.parkrun.org.uk/" + loc + \
                    "/results/weeklyresults/?runSeqNumber=" + str(eid)
        else:
            url = "https://www.parkrun.org.uk/" + loc + \
                    "/results/latestresults/"
        print(url)

        # The html version of the result table
        html_doc = get_URL_content(url)
        soup = BeautifulSoup(html_doc, 'html.parser')

        parkrun_str = str(soup.find("h2"))
        # Pythonic way of removing all whitespaces
        parkrun_str = "".join(parkrun_str.split())
        # Strip the <h2> and </h2> tags, then remove location
        eid_date_str = parkrun_str[4:-5].split('#')[1]
        date_str = eid_date_str.rsplit('-')[1]

        # We want to extract the eid from the webpage itself
        html_eid = int(eid_date_str.split('-')[0])

        self.loc = loc
        self.eid = html_eid
        self.date = date(int(date_str.split('/')[2]),
                         int(date_str.split('/')[1]),
                         int(date_str.split('/')[0]))
        self.tbl = soup_to_tbl(self.loc, self.eid, self.date, soup)

    def __repr__(self):
        txt = "loc: " + self.loc + ", eid: " + str(self.eid) + "\n"
        for i in self.tbl:
            txt += str(i) + "\n"
        return txt
