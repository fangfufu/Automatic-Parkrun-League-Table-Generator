#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Parkrun Result Database
This is a part of Automatic Parkrun League Table Generator
Dedicated to UEA Triathlon Club
"""
import sys
from table import ParkrunEntry, ParkrunTable

class TableAlreadyExist(Exception):
    pass

class ParkrunDB:
    def __init__(self, loc, club_names, eid_start, eid_end):
        self.loc = loc
        self.club_names = club_names
        self.tables = {}
        # eid_end + 1 to compensate for the way range works.
        for eid in range(eid_start, eid_end + 1):
            self.add(eid)

    def add(self, eid):
        if eid not in self.tables:
            self.tables[eid] = ParkrunTable(self.loc, self.club_names, eid)
        else:
            print("ParkrunDB [" + self.loc + "] eid [" + str(eid) +
                  "] already exists.", file=sys.stderr)

    def update(self):
        tbl = ParkrunTable(self.loc, self.club_names, "latest")
        if tbl.eid not in self.tables:
            self.tables[tbl.eid] = tbl
        else:
            print("ParkrunDB [" + self.loc + "] already up-to-date.",
                  file=sys.stderr)

    def __repr__(self):
        txt = ""
        for k in self.tables.keys():
            txt += "loc: " + self.loc + ", eid: " + str(self.tables[k].eid)
            txt += "\n" + str(self.tables[k]) + "\n"
        txt = txt[:-1]
        return txt

class AthleteDB:
    def __init__(self, name):
        self.name = name
        # We use tuple of (loc, eid) as the key for the dictionary
        self.entries = {}
