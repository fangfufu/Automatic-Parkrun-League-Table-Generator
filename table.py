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
        self.fastest = False

    def __repr__(self):
        txt = "|" + str(self.date) + ", " + self.loc + ", " + str(self.eid)
        txt += ", " + str(self.pos) + ", " + self.name + ", "
        txt += sec_to_timestr(self.time) + ", " + str(self.age_grade) + "%, "
        txt += self.gender + ": " + str(self.gender_pos) + ", " + self.club
        txt += ", PB: " + str(self.PB) + "|"
        return txt

class ParkrunTable:
    '''
    The results from a single Parkriun for the selected clubs

    Args:
        loc(str): location of the Parkrun
        club_names(tuple): the name of the club
        eid(int): the Parkrun even number

    Attributes:
        entries (list): List of Parkrun result entries.
    '''
    # NOTE add function to get the fastest athlete for each club
    def __init__(self, loc, eid):
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

        def soup_to_entries(loc, eid, date, soup):
            def html_table_to_entry_list(html_table):
                entry_list = []
                for html_row in html_table.findAll('tr'):
                    html_col = html_row.findAll('td')
                    row = []
                    for column in html_col:
                        row.append(column.text)
                    entry_list.append(row)
                return entry_list

            def remove_unknown(table_row):
                # name is always at the 2nd column
                name = 1
                if not table_row:
                    return False
                if table_row[name] == "Unknown":
                    return False
                else:
                    return True

            html_table = soup.find(id="results")
            if html_table == None:
                raise TableNotFound("Result table not found!")

            entry_list = html_table_to_entry_list(html_table)
            filtered_list = list(filter(remove_unknown, entry_list))

            entries = []
            for i in filtered_list:
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
        self.entries = soup_to_entries(self.loc, self.eid, self.date, soup)

    def __repr__(self):
        txt = "loc: " + self.loc + ", eid: " + str(self.eid) + "\n"
        for i in self.entries:
            txt += str(i) + "\n"
        return txt

    def set_fastest_club_gender(self, clubs):
        for club in clubs:
            for gender in ["M", "F"]:
                def filter_by_club_gender(entry):
                    if entry.gender == gender and entry.club == club:
                        return True
                    else:
                        return False

                sorted_list = sorted(list(filter(filter_by_club_gender,
                                                self.entries)),
                                    key = lambda x : x.time)
                if not sorted_list:
                    continue
                else:
                    print(sorted_list[0])
                    name = sorted_list[0].name

                for entry in self.entries:
                    if entry.name == name:
                        entry.fastest = True

