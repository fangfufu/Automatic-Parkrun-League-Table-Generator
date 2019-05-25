#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Automatic Parkrun League Table Generator
"""

import csv
import requests
import sys
from bs4 import BeautifulSoup
from xml.etree import ElementTree as ET

custom_headers = {
"User-Agent" : ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                "(KHTML, like Gecko) "
                "Chrome/74.0.3729.169 Safari/537.36")
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

def main():
    print("Arguments are: " + str(sys.argv))
    html_doc = get_URL_content(sys.argv[1])
    html_tbl = get_result_table(html_doc)
    list_tbl = table_to_list(html_tbl)

    with open('output.csv', 'w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(list_tbl)

if __name__ == "__main__":
    main()
