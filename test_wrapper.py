#!/usr/bin/python3
# -*- coding: utf-8 -*-
import sys
from util import write_csv, pickle_save, pickle_load
#print("Arguments are: " + str(sys.argv))

from table import ParkrunTable
from database import ParkrunDB, Athlete
club_names = ("University of East Anglia Tri Club",
            "University of East Anglia AC")
#db = ParkrunDB("norwich", club_names, 440, 460)
db = pickle_load("norwich_parkrun_2019.db")
ath = Athlete(db.tables[459].tbl[1])
ath.add_entry(db.tables[459].tbl[1])
