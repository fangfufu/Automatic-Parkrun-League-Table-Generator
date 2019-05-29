#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Utility functions
This is a part of Automatic Parkrun League Table Generator
Dedicated to UEA Triathlon Club
"""
import pickle
import csv
import math
import datetime

def write_csv(lst, fn):
    with open(fn, 'w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(lst)

def pickle_save(data, fn):
    with open(fn, "wb") as pickle_file:
        pickle.dump(data, pickle_file)

def pickle_load(fn):
    with open(fn, "rb") as pickle_file:
        data = pickle.load(pickle_file)
    return data

def sec_to_timestr(sec):
    return str(datetime.timedelta(seconds=sec))

def timestr_to_sec(timestr):
    return int(timestr.split(':')[0]) * 60 + int(timestr.split(':')[1])
