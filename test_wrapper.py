#!/usr/bin/python3
# -*- coding: utf-8 -*-
import sys
from parkrun import ParkrunTable
from util import write_csv, pickle_save, pickle_load

def main():
    # The club name we are checking against
    club_name = ("University of East Anglia Tri Club",
                "University of East Anglia AC")
    print("Arguments are: " + str(sys.argv))
    tbl = ParkrunTable("norwich", club_name, 460)
    print(tbl)
    pickle_save(tbl, 'norwich_parkrun_460.pickle')
    tbl = pickle_load('norwich_parkrun_460.pickle')
    print(tbl)

if __name__ == "__main__":
    main()
