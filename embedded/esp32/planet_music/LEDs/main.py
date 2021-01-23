import gc

import machine, neopixel
import network
import utime as time
import urequests as requests
from credentials import WIFI_SSID, WIFI_PASSWORD, WOLFRAM_API_KEY
from ntptime import settime
from scron.week import simple_cron

#initialize neopixel
n = 9
p = 13
np = neopixel.NeoPixel(machine.Pin(p), n, bpp=4)

def do_connect():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        wlan.connect(WIFI_SSID, WIFI_PASSWORD)
        while not wlan.isconnected():
#            wdt.feed()
            pass
    print('network config:', wlan.ifconfig())

do_connect()
gc.collect()

time.sleep(1)

def make_planet_list():
    for i, name in enumerate (names) :
        # obtain rise time from wolframalpha API
        url = "http://api.wolframalpha.com/v2/result?i={0}%20rise%20today%20unix%20time%3F&appid={1}".format(name, WOLFRAM_API_KEY)
        r = requests.get(url)
        print(r.text)
        rise[i][0] = r.text
        rise[i][0] = [x.strip() for x in rise[i][1].split(' ')]
        rise[i][0] = int(rise[i][0][0]) - 946080000 #convert to embedded Epoch
        r.close()
        del r
        rise[i][1] = name
        rise [i][2] = 'rise'

        # obtain set time from wolframalpha API
        url = "http://api.wolframalpha.com/v2/result?i={0}%20set%20today%20unix%20time%3F&appid={1}".format(name, WOLFRAM_API_KEY)
        r = requests.get(url)
        print(r.text)
        sett[i][0] = r.text
        sett[i][0] = [x.strip() for x in sett[i][1].split(' ')]
        sett[i][0] = int(sett[i][0][0]) - 946080000 #convert to embedded Epoch
        r.close()
        del r
        sett[i][1] = name
        sett [i][2] = 'sett'


    rise = [tuple(l) for l in rise]
    sett = [tuple(l) for l in sett]
    planet_list = rise + sett
    list.sort(planet_list)
    return planet_list

# define variables
names = ['Sun', 'Moon']
# 'Mercury', 'Venus', 'Mars', 'Jupiter', 'Saturn', 'Uranus', 'Neptune'
rise = [[0 for i in range(3)] for j in range(len(names))]
sett = [[0 for i in range(3)] for j in range(len(names))]
# note list for each body
LED = [(255, 255, 0, 128),
       (50, 50, 50, 64),
       (212, 102, 102, 0),
       (241, 232, 184, 0),
       (46, 118, 255, 0),
       (255, 0, 0, 0),
       (250, 149, 0, 0),
       (255, 218, 198, 0),
       (54, 65, 86, 0),
       (70, 35, 206, 0)]

# set the RTC
settime()

simple_cron.run()
# set the time once every hour
simple_cron.add(
    'Hourly',
    lambda *a,**k: settime(),
    hours=0,
    minutes=0,
    seconds=0
)

# return time since the Epoch (embedded)

time.sleep(1)

planet_list = make_planet_list()

for timestamp, planetname, action in planet_list:
    # sleep until timestamp
    now = int(time.time())
    print(now)
    time.sleep(timestamp - now)

    if planetname == "Sun" and action == "rise":
        np[0] = LED[0]
    if planetname == "Sun" and action == "sett":
        np[0] = (0, 0, 0, 0)
    if planetname == "Moon" and action == "rise":
        np[1] = LED[1]
    if planetname == "Moon" and action == "sett":
       np[1] = (0, 0, 0, 0)
    if planetname == "Mercury" and action == "rise":
        np[2] = LED[2]
    if planetname == "Mercury" and action == "sett":
        np[2] = (0, 0, 0, 0)
    if planetname == "Venus" and action == "rise":
        np[3] = LED[3]
    if planetname == "Venus" and action == "sett":
        np[3] = (0, 0, 0, 0)
    if planetname == "Mars" and action == "rise":
        np[4] = LED[4]
    if planetname == "Mars" and action == "sett":
        np[4] = (0, 0, 0, 0)
    if planetname == "Jupiter" and action == "rise":
        np[5] = LED[5]
    if planetname == "Jupiter" and action == "sett":
        np[5] = (0, 0, 0, 0)
    if planetname == "Saturn" and action == "rise":
        np[6] = LED[6]
    if planetname == "Saturn" and action == "sett":
        np[6] = (0, 0, 0, 0)
    if planetname == "Uranus" and action == "rise":
        np[7] = LED[7]
    if planetname == "Uranus" and action == "sett":
        np[7] = (0, 0, 0, 0)
    if planetname == "Neptune" and action == "rise":
        np[8] = LED[8]
    if planetname == "Neptune" and action == "sett":
        np[8] = (0, 0, 0, 0)
