# coding: utf-8

from astropy.time import Time
import pandas as pd
import numpy as np

import matplotlib.pyplot as plt 
import matplotlib.dates as dates
import matplotlib

from datetime import *
import math

from altair import *
import callhorizons

def getReferenceMagnitudesFromHorizons(bodyName, epochStart, epochStop):
    horizons = callhorizons.query(bodyName)
    horizons.set_epochrange(epochStart, epochStop, '1h')
    horizons.get_ephemerides(500) #TODO: make observatory configurable?
    return pd.DataFrame({ 'date' : horizons['datetime'], 'APmag' : horizons['V']})

def getHorizonsIntervalsForDates(dateList):
    intervals = []
    currentIntervalStart = None

    for date in dateList:
        if currentIntervalStart is None:
            currentIntervalStart = date
            nextDay = datetime.strptime(currentIntervalStart, '%Y-%m-%d') + timedelta(days=1)
            continue

        d = datetime.strptime(date, '%Y-%m-%d')
        if (d == nextDay):
            nextDay = nextDay + timedelta(days=1)
        else:
            intervals.append((currentIntervalStart, datetime.strftime(nextDay, '%Y-%m-%d')))
            currentIntervalStart = date
            nextDay = datetime.strptime(date, '%Y-%m-%d') + timedelta(days=1)

    if not currentIntervalStart is None:
        intervals.append((currentIntervalStart, datetime.strftime(nextDay, '%Y-%m-%d')))

    return intervals

def timeFromDecimalDaytime(t):
    date = t[0:10].replace(' ', '-')
    timeOfDay = float('0' + t[10:])
    rest, hour = math.modf(timeOfDay * 24)
    rest, minute = math.modf(rest * 60)
    rest, second = math.modf(rest * 60)
    time = str(int(hour)) + ':' + str(int(minute)) + ':' + str(int(second))# + str(rest)[0:4]
    t = Time(date + 'T' + time, format='isot', scale='utc')
    return t