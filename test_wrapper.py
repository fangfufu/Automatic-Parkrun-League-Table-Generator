#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import json
from parkrun_url import get_parkrun_result

def write_list_as_csv(lst, fn):
    with open(fn, 'w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(lst)

def gen_parkrun_db(loc, club_name, start, end):
    parkrun_db = {}
    for i in range(start, end):
        parkrun_db[str(i)] = get_parkrun_result(loc, club_name, str(i))
    return parkrun_db

def json_save(data, fn):
    with open(fn, 'w') as outfile:
        json.dump(data, outfile)

def json_load(fn):
    with open(fn) as json_file:
        data = json.load(json_file)
    return data

def main():
    # The club name we are checking against
    club_name = ("University of East Anglia Tri Club",
                "University of East Anglia AC")
    print("Arguments are: " + str(sys.argv))
    parkrun_db = gen_parkrun_db("norwich", club_name, 455, 460)
    #print(parkrun_db)
    json_save(parkrun_db, 'norwich_parkrun_db.json')
    ftbl = parkrun_db['455']
    print(ftbl)
    parkrun_db = json_load('norwich_parkrun_db.json')
    #print(parkrun_db)
    ftbl = parkrun_db['455']
    print(ftbl)
    #write_list_as_csv(ftbl, sys.argv[2])

if __name__ == "__main__":
    main()
