#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Parkrun Result Database
This is a part of Automatic Parkrun League Table Generator
Dedicated to UEA Triathlon Club
"""

import sys
from collections import OrderedDict
from table import ParkrunEntry, ParkrunTable

class WrongAthlete(Exception):
    pass

class AthleteDoesNotExist(Exception):
    pass

class ParkrunDB:
    def __init__(self, loc, club_names, eid_start, eid_end):
        self.loc = loc
        self.club_names = club_names
        self.tables = {}
        # eid_end + 1 to compensate for the way range works.
        for eid in range(eid_start, eid_end + 1):
            self.add(eid)

    def __repr__(self):
        txt = ""
        for k in self.tables.values():
            txt += str(k)
        return txt

    def add(self, eid):
        if eid not in self.tables:
            self.tables[eid] = ParkrunTable(self.loc, self.club_names, eid)
        else:
            print("ParkrunDB [" + self.loc + "] eid [" + str(eid) +
                  "] already exists.", file = sys.stderr)

    def clear(self):
        self.tables.clear()

    def update(self):
        table = ParkrunTable(self.loc, self.club_names, "latest")
        if table.eid not in self.tables:
            self.tables[table.eid] = table
        else:
            print("ParkrunDB [" + self.loc + "] already up-to-date.",
                  file = sys.stderr)
        return table.eid

class Athlete:
    def __init__(self, name, club):
        self.name = name
        self.club = club
        # We use tuple of (loc, eid) as the key for the dictionary
        self.entries = OrderedDict()

    def __repr__(self):
        txt = "Athlete: " + self.name + "\n"
        for i in self.entries.values():
            txt += str(i) + "\n"
        txt = txt[:-1]
        return txt

    def add_entry(self, entry):
        if self.name == entry.name:
            if (entry.loc, entry.eid) not in self.entries:
                self.entries[(entry.loc, entry.eid)] = entry
            else:
                print("Athlete [" + self.name + "]: entry (" + entry.loc, ", " +
                      entry.eid + ") already exists.", file = sys.stderr)
        else:
            raise WrongAthlete("Attempted to add entry to the wrong athlete")

    def clear(self):
        self.entries.clear()

    def sort_entries(self):
        self.entries = OrderedDict(sorted(self.entries.items(),
                                    key = lambda x : x[1].date))

    def time(self):
        return [entry.time for entry in self.entries.values()]

    def age_grade(self):
        return [entry.age_grade for entry in self.entries.values()]

    def PB(self):
        return [entry.PB for entry in self.entries.values()].count(True)

    def loc(self):
        return [entry.loc for entry in self.entries.values()]

    def date(self):
        return [entry.date for entry in self.entries.values()]

    def attendance(self):
        return len(self.entries)

    # def sort_entries(self):
    # NOTE: Add function to sort entries by date

class AthleteDB:
    def __init__(self):
        self.athletes = OrderedDict()

    def __repr__(self):
        return str(list(self.athletes.keys()))

    def add_athlete(self, athlete):
        if athlete.name not in self.athletes:
            self.athletes[(athlete.name)] = athlete
        else:
            print("Athlete["+ athlete.name +"] already in the database.",
                  file=sys.stderr)

    def del_athlete(self, athlete_name):
        if athlete_name in self.athletes:
            athletes.pop(athlete_name, None)
        else:
            raise AthleteDoesNotExist("Athlete[" + athlete_name +
                                      "] does not exist.")
    def clear(self):
        self.athletes.clear();

    def sort_athlete_entries(self):
        for athlete in self.athletes.values():
            athlete.sort_entries()

    def populate(self, parkrun_db):
        for parkrun_table in parkrun_db.tables.values():
            for parkrun_entry in parkrun_table.table:
                if parkrun_entry.name not in self.athletes:
                    self.add_athlete(Athlete(parkrun_entry.name,
                                             parkrun_entry.club))
                self.athletes[parkrun_entry.name].add_entry(parkrun_entry)
        self.sort_athlete_entries()

    def league_table(self):
        '''Print the attendance and PB of each athlete.'''
        attending_score = 2
        PB_score = 3
        tbl = [["Name", "Club", "Attendance", "PB", "Score"]]
        tbl_content = [];
        for athlete in self.athletes.values():
            tbl_content.append([athlete.name, athlete.club,
                                athlete.attendance(), athlete.PB(),
                                athlete.attendance() * attending_score +
                                athlete.PB() * PB_score])
        # The 5th column is the parkrun score.
        tbl_content = sorted(tbl_content, key = lambda x : x[4], reverse=True)
        tbl.extend(tbl_content)
        return tbl
