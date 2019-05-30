#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Scrap code
#import sys
#print("Arguments are: " + str(sys.argv))
#db = ParkrunDB("norwich", club_names, 440, 460)
#club_names = ("University of East Anglia Tri Club",
            #"University of East Anglia AC")

from util import pickle_save, pickle_load
from database import ParkrunDB, AthleteDB
parkrun_db = pickle_load("norwich_parkrun_2019.db")
athlete_db = AthleteDB()
athlete_db.populate(parkrun_db)
