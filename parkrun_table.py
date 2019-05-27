#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Parkrun Result Table Downloader
This is a part of Automatic Parkrun League Table Generator
Dedicated to UEA Triathlon Club
"""
import csv
import requests
import sys
from bs4 import BeautifulSoup
from util import sec_to_timestr, timestr_to_sec

class HTTPError(Exception):
    pass

class TableNotFound(Exception):
    pass

class ParkrunTableEntry:
    def __init__(self, entry):
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

    def __repr__(self):
        txt = "|" + self.name + "\t"
        txt = txt.expandtabs(20)
        txt += self.gender + ": " + str(self.gender_pos) + "\t"
        txt = txt.expandtabs(4)
        txt += self.club + "\t"
        txt = txt.expandtabs(8)
        txt += "PB: " + str(self.PB) + "\t|"
        txt = txt.expandtabs(4)
        return txt

class ParkrunTable:
    '''
    The results from a single Parkriun for the selected clubs

    Args:
        loc(str): location of the Parkrun
        club_name(tuple): the name of the club
        eid(int): the Parkrun even number

    Attributes:
        tbl (list): List of Parkrun result entries.
    '''
    def __init__(self, loc, club_name, eid):
        # Generate the URL
        if str(eid) != "latest":
            url = "https://www.parkrun.org.uk/" + loc + \
                    "/results/weeklyresults/?runSeqNumber=" + str(eid)
        else:
            url = "https://www.parkrun.org.uk/" + loc + \
                    "/results/latestresults/"
        print(url)

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

        # The html version of the result table
        html_doc = get_URL_content(url)

        def html_to_tbl(html_doc):
            soup = BeautifulSoup(html_doc, 'html.parser')
            html_tbl = soup.find(id="results")
            if html_tbl == None:
                raise TableNotFound("Result table not found!")

            def html_tbl_to_list_tbl(html_tbl):
                list_tbl = []
                for html_row in html_tbl.findAll('tr'):
                    html_col = html_row.findAll('td')
                    row = []
                    for column in html_col:
                        row.append(column.text)
                    list_tbl.append(row)
                return list_tbl

            list_tbl = html_tbl_to_list_tbl(html_tbl)

            def filter_by_club(tbl_row):
                # Club name is always at the 8th column
                club = 7
                if not tbl_row:
                    return False
                if tbl_row[club] in club_name:
                    return True
                else:
                    return False

            filtered_tbl = list(filter(filter_by_club, list_tbl))

            entries = []
            for i in filtered_tbl:
                entries.append(ParkrunTableEntry(i))
            return entries

        self.tbl = html_to_tbl(html_doc)

    def __repr__(self):
        txt = "|Name\t\t\t\tG: Pos\tClub\t\t\t\t\t\t\t\tPB\t\t\t|\n"
        txt = txt.expandtabs(4)
        for i in self.tbl:
            txt += str(i) + "\n"
        txt = txt[:-1]
        return txt

