#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Automatic Parkrun League Table Generator
Dedicated to UEA Triathlon Club
"""
import csv
import requests
import sys
from bs4 import BeautifulSoup

# Custom user-agent because Parkrun doesn't like webscraping. 
# (We are being naughty)
custom_headers = {
"User-Agent" : ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                "(KHTML, like Gecko) "
                "Chrome/74.0.3729.169 Safari/537.36")
}

# The row name of the result table
rn = {"pos" : 0,
        "name" : 1,
        "time" : 2,
        "age_cat" : 3,
        "age_grade" : 4,
        "gender" : 5,
        "gender_pos" : 6,
        "club" : 7,
        "note" : 8,
        "total" : 9
        }

class HTTPError(Exception):
    pass

class TableNotFound(Exception):
    pass

def get_URL_content(url):
    """Get the content of a URL."""

    r = requests.get(url, headers=custom_headers)
    if r.status_code != 200:
        raise HTTPError("Http Error, status code: " + str(r.status_code))
    return r.text

def get_result_table(html_doc):
    soup = BeautifulSoup(html_doc, 'html.parser')
    tbl = soup.find(id="results")
    if tbl == None:
        raise TableNotFound("Result table not found!")
    return tbl

def table_to_list(table):
    output_rows = []
    for table_row in table.findAll('tr'):
        columns = table_row.findAll('td')
        output_row = []
        for column in columns:
            output_row.append(column.text)
        output_rows.append(output_row)
    return output_rows

def parkrun_url_constructor(loc, eid):
    if eid != "latest":
        return "https://www.parkrun.org.uk/" + loc + \
                "/results/weeklyresults/?runSeqNumber=" + eid
    else:
        return "https://www.parkrun.org.uk/" + loc + "/results/latestresults/"

def get_parkrun_result(loc, eid, club_name):
    url = parkrun_url_constructor(loc, eid)
    html_doc = get_URL_content(url)
    html_tbl = get_result_table(html_doc)
    parsed_tbl = table_to_list(html_tbl)

    def table_filter_by_club(tbl_row):
        if not tbl_row:
            return False
        if tbl_row[rn["club"]] in club_name:
            return True
        else:
            return False

    filtered_tbl = list(filter(table_filter_by_club, parsed_tbl))
    return filtered_tbl
