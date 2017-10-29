"""
Nicholas A Miller
27 October 2017

Problem 019

You are given the following information, but you may prefer to do some research for yourself.

1 Jan 1900 was a Monday.
Thirty days has September,
April, June and November.
All the rest have thirty-one,
Saving February alone,
Which has twenty-eight, rain or shine.
And on leap years, twenty-nine.
A leap year occurs on any year evenly divisible by 4, but not on a century unless it is divisible by 400.
How many Sundays fell on the first of the month during the twentieth century (1 Jan 1901 to 31 Dec 2000)?
"""

from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

def get_sunday_firsts(earliest, latest):
    """Count Sunday the 1sts between earliest and latest
    Inputs:
        earliest: datetime object of earliest date
        latest: datetime object of latest date
    Returns:
        number of sunday-the-firsts (as int)
    """
    sunday_firsts = list()
    current_date = earliest

    while current_date < latest:
        if current_date.day == 1 and current_date.weekday() == 6:
            sunday_firsts.append(current_date)
        current_date += relativedelta(months=1)
    return len(sunday_firsts)

if __name__ == "__main__":
    earliest = datetime(1901, 1, 1)
    latest = datetime(2000, 12, 31)
    sunday_firsts = get_sunday_firsts(earliest, latest)
    print(sunday_firsts)
    assert sunday_firsts == 171 #Test that it works
    print("OK!")
