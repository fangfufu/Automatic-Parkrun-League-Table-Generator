#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Parkrun Result Database
This is a part of Automatic Parkrun League Table Generator
Dedicated to UEA Triathlon Club
"""

import random
import sys
import time
from collections import OrderedDict
from table import ParkrunEntry, ParkrunTable

class WrongAthlete(Exception):
    pass

class AthleteDoesNotExist(Exception):
    pass

class ParkrunDB:
    def __init__(self, loc, eid_start, eid_end, delay=10):
        self.loc = loc
        self.tables = OrderedDict()
        self.delay = delay
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
            self.tables[eid] = ParkrunTable(self.loc, eid)
            actual_delay = random.randint(1, self.delay)
            time.sleep(actual_delay)
            print("ParkrunDB [" + self.loc + "]: delaying " + str(actual_delay)
                  + " secs", file = sys.stderr)
        else:
            print("ParkrunDB [" + self.loc + "] eid [" + str(eid) +
                  "] already exists.", file = sys.stderr)

    def clear(self):
        self.tables.clear()

    def update(self):
        table = ParkrunTable(self.loc, "latest")
        self.tables = OrderedDict(sorted(self.tables.items(),
                                         key = lambda x : x[0]))
        if table.eid not in self.tables:
            for eid in range(
                list(self.tables.items())[len(self.tables) - 1][0] + 1,
                                                           table.eid + 1):
                self.add(eid)
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

    def fastest(self):
        return [entry.fastest for entry in self.entries.values()].count(True)

    def loc(self):
        return [entry.loc for entry in self.entries.values()]

    def date(self):
        return [entry.date for entry in self.entries.values()]

    def attendance(self):
        return len(self.entries)

class AthleteDB:
    def __init__(self, club_names):
        self.athletes = OrderedDict()
        self.clubs = club_names

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
            parkrun_table.set_fastest_club_gender(self.clubs)
            for entry in parkrun_table.entries:
                if entry.club not in self.clubs:
                    continue
                if entry.name not in self.athletes:
                    self.add_athlete(Athlete(entry.name, entry.club))
                self.athletes[entry.name].add_entry(entry)
        self.sort_athlete_entries()

    def league_table(self):
        '''Print the attendance and PB of each athlete.'''
        attendance_score = 2
        PB_score = 3
        fastest_score = 3
        tbl = [["Name", "Club", "Attendance", "PB", "Fastest", "Score"]]
        tbl_content = [];
        for athlete in self.athletes.values():
            tbl_content.append([athlete.name, athlete.club,
                                athlete.attendance(), athlete.PB(),
                                athlete.fastest(),
                                athlete.attendance() * attendance_score +
                                athlete.PB() * PB_score +
                                athlete.fastest() * fastest_score])
        # The 5th column is the parkrun score.
        tbl_content = sorted(tbl_content, key = lambda x : x[4], reverse=True)
        tbl.extend(tbl_content)
        return tbl
