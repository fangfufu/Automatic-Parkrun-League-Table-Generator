#!/usr/bin/python3
# -*- coding: utf-8 -*-
import sys
from table import ParkrunTable
from database import ParkrunDB
from util import write_csv, pickle_save, pickle_load

def main():
    # The club name we are checking against
    club_names = ("University of East Anglia Tri Club",
                "University of East Anglia AC")
    print("Arguments are: " + str(sys.argv))
    db = ParkrunDB("norwich", club_names, 458, 459)
    db.update()
    db.update()
    print(db)
    pickle_save(db, 'ParkrunDB.pickle')
    db = pickle_load('ParkrunDB.pickle')
    print(db)

if __name__ == "__main__":
    main()
