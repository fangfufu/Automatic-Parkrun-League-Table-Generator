#!/usr/bin/python3
# -*- coding: utf-8 -*-

from util import pickle_save
from database import ParkrunDB

#norwich_db = ParkrunDB("norwich", 440, 441)
#norwich_db.update()
#pickle_save(norwich_db, 'norwich_parkrun_2019.db')

colneylane_db = ParkrunDB("colneylane", 56, 57)
colneylane_db.update()
pickle_save(colneylane_db, 'colneylane_parkrun_2019.db')
