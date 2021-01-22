import gc


import network
import utime as time
import urequests as requests
from credentials import WIFI_SSID, WIFI_PASSWORD, WOLFRAM_API_KEY
from ntptime import settime


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
settime()

now = time.localtime(time.mktime(time.localtime()) - 5*3600)
print(now)
time.sleep(1)


# this file will get the day's rise/set times and light up LEDs for that day

names = ['Sun', 'Moon', 'Mercury', 'Venus', 'Mars', 'Jupiter', 'Saturn', 'Uranus', 'Neptune']
rise = [0 for i in range(len(names))]
sett = [0 for i in range(len(names))]


for index1, name in enumerate (names) :

    # obtain rise time from wolframalpha API
    url = "http://api.wolframalpha.com/v1/result?i={0}%20rise%3F&appid={1}".format(name, WOLFRAM_API_KEY)
    r = requests.get(url)
    print(r.text)
    rise[index1] = r.text
    r.close()
    del r

    # obtain set time from wolframalpha API
    url = "http://api.wolframalpha.com/v1/result?i={0}%20set%3F&appid={1}".format(name, WOLFRAM_API_KEY)
    r = requests.get(url)
    print(r.text)
    sett[index1] = r.text
    r.close()
    del r


#parse sunrise strings, which start with "at "
#parse string by spaces
rise[0] = [x.strip() for x in rise[0].split(' ')]
sett[0] = [x.strip() for x in sett[0].split(' ')]
#delete "at " from list
del rise[0][0]
del sett[0][0]

#parse all other strings
for i in range(len(names) - 1):
    #parse string by spaces
    rise[i+1] = [x.strip() for x in rise[i+1].split(' ')]
    sett[i+1] = [x.strip() for x in sett[i+1].split(' ')]

#parse whole list, convert to 24h time and keep only the hour and minute
for i in range(len(names)):
    if rise[i][1] == 'A.M.':
        rise[i] = rise[i][0] + ' AM'
    else:
        rise[i] = rise[i][0] + ' PM'

    if sett[i][1] == 'A.M.':
        sett[i] = sett[i][0] + ' AM'
    else:
        sett[i] = sett[i][0] + ' PM'

    # rise[i] = datetime.strptime(rise[i], "%I:%M %p")
    # sett[i] = datetime.strptime(sett[i], "%I:%M %p")

    # rise[i] = int(datetime.strftime(rise[i], "%H"))
    # sett[i] = int(datetime.strftime(sett[i], "%H"))