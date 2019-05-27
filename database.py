#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Parkrun Database related functions
This is a part of Automatic Parkrun League Table Generator
Dedicated to UEA Triathlon Club
"""
from parkrun_table import get_parkrun_result

def gen_parkrun_db(loc, club_name, start, end):
    parkrun_db = {}
    for i in range(start, end):
        parkrun_db[i] = get_parkrun_result(loc, club_name, i)
    return parkrun_db
