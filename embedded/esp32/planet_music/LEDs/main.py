import gc


import network
import utime as time
import urequests as requests
from credentials import WIFI_SSID, WIFI_PASSWORD, WOLFRAM_API_KEY
from ntptime import settime
from scron.week import simple_cron

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
        rise[i][1] = r.text
        rise[i][1] = [x.strip() for x in rise[i][1].split(' ')]
        rise[i][1] = int(rise[i][1][0]) - 946080000 #convert to embedded Epoch
        r.close()
        del r
        rise[i][0] = rise[i][1] - now #seconds from "now" until event
        rise[i][2] = name
        rise [i][3] = 'rise'

        # obtain set time from wolframalpha API
        url = "http://api.wolframalpha.com/v2/result?i={0}%20set%20today%20unix%20time%3F&appid={1}".format(name, WOLFRAM_API_KEY)
        r = requests.get(url)
        print(r.text)
        sett[i][1] = r.text
        sett[i][1] = [x.strip() for x in sett[i][1].split(' ')]
        sett[i][1] = int(sett[i][1][0]) - 946080000 #convert to embedded Epoch
        r.close()
        del r
        sett[i][0] = sett[i][1] - now #seconds from "now" until event
        sett[i][2] = name
        sett [i][3] = 'sett'


    rise = [tuple(l) for l in rise]
    sett = [tuple(l) for l in sett]
    planet_list = rise + sett
    list.sort(planet_list)

# define variables
names = ['Sun', 'Moon']
# 'Mercury', 'Venus', 'Mars', 'Jupiter', 'Saturn', 'Uranus', 'Neptune'
rise = [[0 for i in range(4)] for j in range(len(names))]
sett = [[0 for i in range(4)] for j in range(len(names))]

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
now = int(time.time())
print(now)
time.sleep(1)

make_planet_list()



sorted_planet_time_list = [(12345, "mars", "rise")]
for timestamp, planetname, action in sorted_planet_time_list:
    # sleep until timestamp
    if planetname == "mars" and action == "rise":
        #whatever
