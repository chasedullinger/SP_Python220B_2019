#!/usr/env/bin python
"""
Documentation for make_more_data.py

This file will make more records matching the format in exercise.csv

5df44a54-8cca-4928-bc53-caabb23cf329,1,2,3,4,05/26/2015,

[7]-[4]-[4]-[4]-[12],n  ,n+1,n+2,n+3,MM/DD/YYYY,[ao]
[7]-[4]-[4]-[4]-[12],n+1,n+2,n+3,n+4,MM/DD/YYYY,[ao]

"""
import os
import uuid
import time
import random
from datetime import datetime

lines = []
tstart = time.time()
file = "exercise.csv"
pathx = r"C:\Users\pants\PycharmProjects\SP_Python220B_2019\students\
            tim_lurvey\lesson06\assignment\data"


def rand_pattern(n):
    """generate the random patten as follows:
    uuid4(),n,n+1,n+2,n+3,MM/DD/YYYY,[ao]"""
    rand_epoch = int(random.randint(1000000000,
                                    datetime(2018, 12, 31, 12, 59).timestamp()))
    for x in [str(uuid.uuid4()),
              n,
              n + 1,
              n + 2,
              n + 3,
              datetime.fromtimestamp(rand_epoch).strftime("%m/%d/%Y"),
              random.choice(("", "ao")),
              ]:
        yield str(x)


for i in range(11, 1000001):
    # for i in range(11,21):
    lines.append('\n' + ','.join(rand_pattern(i)))
    if not i % 10000:
        print(f"{i:>7d} @ {time.time() - tstart} seconds")

with open(os.path.join(pathx, file), 'a') as A:
    A.writelines(lines)

print(f"this took {time.time() - tstart} seconds")
