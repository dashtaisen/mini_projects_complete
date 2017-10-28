"""
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

import datetime

earliest = datetime.datetime(1901, 1, 1)
latest = datetime.datetime(2000, 12, 31)

dates = [earliest + datetime.timedelta(days=x) for x in range((latest-earliest).days + 1)]
sunday_firsts = [date for date in dates if date.day == 1 and date.weekday() == 6]
