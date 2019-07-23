#!//bin/env python
import ephem
import time
import datetime
import struct,os,sys
import numpy as np
import math
from math import pi
import matplotlib.pyplot as plt

n=365*2
days = np.linspace(0,n,n)*0
#days = np.linspace(0,1,20000)
moon_size = days*0.0
moon_distance = days*0.0

ant = ephem.Observer()
ant.long = '106:51:24.0'
ant.lat = '25:39:10.6'
ant.elevation = 1110.0288
 
#site = ephem.Observer()
#site.lat = '25.652939'
#site.lon = '106.856594'

date0 = ant.date

src = ephem.Moon()
sun = ephem.Sun()
for i in range(n):
  #print ant.date
  src.compute(ant)
  t_next_transit = ant.next_transit(src)
  days[i] = t_next_transit 
  moon_size[i] = src.size/60
  moon_distance[i] = src.earth_distance*ephem.meters_per_au/1000
  ant.date = t_next_transit
  sun.compute(ant)
  if float(src.dec)/pi*180 >25:
    print t_next_transit, "\t", src.ra, "\t", src.dec, src.radius/pi*180*60*2, src.size/60,  "\t", ant.date, sun.ra, sun.dec
 
fig = plt.figure()
l, = plt.plot(days, moon_size, '-')
#l, = plt.plot(days, 'ro')
#plt.xlim(0, 1)
#plt.ylim(0, 1)
plt.xlabel('day')
#plt.ylabel('distance (km)')
plt.ylabel('moon size (arcmin)')
fig.savefig("transit_size.png")
plt.show()

