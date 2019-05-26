#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
from parkrun_url import get_parkrun_result

def write_list_as_csv(lst, fn):
    with open(fn, 'w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(lst)

def gen_league_table(loc, start, end):
    return 0

def league_table_append(loc):
    return 0

def main():
    # The club name we are checking against
    club_name = ("University of East Anglia Tri Club",
                "University of East Anglia AC")
    print("Arguments are: " + str(sys.argv))
    ftbl = get_parkrun_result(sys.argv[1], sys.argv[2], club_name)
    print(ftbl)
    #write_list_as_csv(ftbl, sys.argv[2])

if __name__ == "__main__":
    main()
