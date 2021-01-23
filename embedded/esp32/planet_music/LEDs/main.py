import gc

import machine, neopixel
import network
import utime as time
import urequests as requests
from credentials import WIFI_SSID, WIFI_PASSWORD, WOLFRAM_API_KEY
from ntptime import settime
# from scron.week import simple_cron

time.sleep(1)

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

def planet_timestamp(name, action):
    url = "http://api.wolframalpha.com/v2/result?i={0}%20{1}%20next%20unix%20time%3F&appid={2}".format(name, action, WOLFRAM_API_KEY)
    r = requests.get(url)
    print(r.text)
    timestamp = r.text
    timestamp = [x.strip() for x in timestamp.split(' ')]
    timestamp = int(timestamp[0]) - 946080000 #convert to embedded Epoch
    r.close()
    del r
    return timestamp

def make_planet_list():
    for i, name in enumerate(names) :
        # obtain rise time from wolframalpha API
        rise[i][0] = planet_timestamp(name, 'rise')
        rise[i][1] = name
        rise[i][2] = 'rise'

        # obtain set time from wolframalpha API
        sett[i][0] = planet_timestamp(name, 'set')
        sett[i][1] = name
        sett[i][2] = 'sett'

    rise = [tuple(l) for l in rise]
    sett = [tuple(l) for l in sett]
    planet_list = rise + sett
    list.sort(planet_list)
    return planet_list

# define variables
names = ['Sun', 'Moon', 'Mercury', 'Venus', 'Mars', 'Jupiter', 'Saturn', 'Uranus', 'Neptune']
rise = [[0 for i in range(3)] for j in range(len(names))]
sett = [[0 for i in range(3)] for j in range(len(names))]
# LED list for each body
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

# simple_cron.run()
# # set the time once every hour
# simple_cron.add(
#     'Hourly',
#     lambda *a,**k: settime(),
#     minutes=0,
#     seconds=0
# )

time.sleep(1)

planet_list = make_planet_list()

while True:
    timestamp, planetname, action = planet_list.pop(0)
    # sleep until timestamp
    now = int(time.time()) # return time since the Epoch (embedded)
    print(now)
    time.sleep(timestamp - now)

    planet_num = names.index(planetname)
    if action == "rise":
        np[planet_num] = LED[planet_num]
        next_timestamp = planet_timestamp(planetname, 'rise')
        next_tuple = (next_timestamp, planetname, 'rise')

    elif action == "sett":
        np[planet_num] = (0, 0, 0, 0)
        next_timestamp = planet_timestamp(planetname, 'set')
        next_tuple = (next_timestamp, planetname, 'sett')

    planet_list.append(next_tuple)
    list.sort(planet_list)
