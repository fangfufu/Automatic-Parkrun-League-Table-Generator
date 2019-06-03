#!/usr/bin/python3
# -*- coding: utf-8 -*-

from util import pickle_save, pickle_load, write_csv
from database import ParkrunDB, AthleteDB

club_names = ("University of East Anglia Tri Club",
             "University of East Anglia AC")
norwich_db = pickle_load("norwich_parkrun_2019.db")
colneylane_db = pickle_load("colneylane_parkrun_2019.db")
athlete_db = AthleteDB(club_names)
athlete_db.populate(norwich_db)
athlete_db.populate(colneylane_db)
write_csv(athlete_db.league_table(), "output.csv")
