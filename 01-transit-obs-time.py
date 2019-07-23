#!//bin/env python
import ephem
import time
import datetime
import struct,os,sys
import numpy as np
import math
from math import pi
import matplotlib.pyplot as plt

print '=== len(sys.argv) =', len(sys.argv)
date = None;
if len(sys.argv) == 1:
    time0 = time.strftime("%Y/%m/%d  %H:%M:%S", time.localtime(time.time()))
    time0_gmt = time.strftime("%Y/%m/%d  %H:%M:%S", time.gmtime(time.time()))
    print "Local time:", time0
    print "GMT   time:", time0_gmt
elif len(sys.argv) == 2:
    time0 = sys.argv[1]    
else:
        print('Usage: %s YYYY/MM/DD' % sys.argv[0])
        print """
              input like:
                2017/07/29
              """ 
        exit()


n=7
days = np.linspace(0,1,n)*0.0
moon_size = days*0.0
moon_distance = days*0.0


ant = ephem.Observer()
ant.long = '106:51:24.0'
ant.lat = '25:39:10.6'
ant.elevation = 1110.0288

#this may be old, need check 
#site = ephem.Observer()
#site.lat = '25.652939'
#site.lon = '106.856594'

print "receiver rotate 30 deg"

beam_width = .27/2/(.4621*300)/pi*180*60
print "Beam width:", beam_width

ant.date= time0
date0 = ant.date
print "\n===Next few transit:"
print "date", "\t", "  GMT time", "\t", "data record time", "\t", "RA     ", "\t", "Dec     ", "\t",  "radius"
src = ephem.Moon()
sun = ephem.Sun()
for i in range(len(days)):
  src.compute(ant)
  sun.compute(ant)
  moon_distance[i] = src.earth_distance*ephem.meters_per_au/1000
  moon_size[i] = src.size/60
  t_next_transit = ant.next_transit(src)
  delta_ang_arcmin = src.radius/pi*180*60 - (2*beam_width*3.0**0.5/2.0 - beam_width/2.0)
  delta_t  = delta_ang_arcmin/math.cos(src.dec)*60/15
  #print delta_ang_arcmin, delta_t
  #print t_next_transit,  "\t", src.ra, "\t", src.dec, "\t", src.radius/pi*180*60, "\t", sun.ra, "\t", sun.dec
  print t_next_transit, "\t", ephem.date(t_next_transit-delta_t/24/3600), "\t", src.ra, "\t", src.dec, "\t", src.radius/pi*180*60, "\t", sun.ra, "\t", sun.dec
  
  ant.date = t_next_transit  

fig = plt.figure()
plt.plot(days, moon_size, '-')
#l, = plt.plot(days, 'ro')
#plt.xlim(0, 1)
#plt.ylim(0, 1)
plt.xlabel('day')
plt.ylabel('distance (km)')
#plt.ylabel('size (arcmin)')
fig.savefig("moon_size.png")
#plt.show()

