import gc

import ssd1306
import gfx
import machine, neopixel
from machine import I2C, Pin
import network
import utime as time
import urequests as requests
from credentials import WIFI_SSID, WIFI_PASSWORD, WOLFRAM_API_KEY
from ntptime import settime
# from scron.week import simple_cron
import ubinascii
mac = ubinascii.hexlify(network.WLAN().config('mac'),':').decode()
print(mac)

time.sleep(1)

#initialize display and graphics
oled_reset_pin = Pin(16, Pin.OUT)
oled_reset_pin.value(1)
time.sleep(1)
i2c = I2C(scl=Pin(15), sda=Pin(4))
time.sleep(1)
oled = ssd1306.SSD1306_I2C(128, 64, i2c)
time.sleep(1)
graphics = gfx.GFX(128, 64, oled.pixel)
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
            pass
    print('network config:', wlan.ifconfig())

do_connect()
gc.collect()

oled.fill(0)
oled.text('wifi connected',0,0,1)
oled.show()
time.sleep(1)


def planet_timestamp(name, action):
    url = "http://api.wolframalpha.com/v1/result?i={0}%20{1}%20next%20unix%20time%3F&appid={2}".format(name, action, WOLFRAM_API_KEY)
    print(url)
    r = requests.get(url)
    print(r.text)
    timestamp = r.text
    timestamp = [x.strip() for x in timestamp.split(' ')]
    timestamp = int(timestamp[0]) - 946684800 #convert to embedded Epoch
    r.close()
    del r
    return timestamp

def make_planet_list():
    rise = [[0 for i in range(3)] for j in range(len(names))]
    sett = [[0 for i in range(3)] for j in range(len(names))]
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
def set_time_with_retry(retries):
    while True:
        if retries == 0:
            return
        try:
            settime()
            print('settime successful')
        except:
            retries -= 1
            time.sleep(5)
            print('retries remaining: {}'.format(retries))
        else:
            return

set_time_with_retry(3)

now = int(time.time()) # return time since the Epoch (embedded)
print(now)
now_local = time.localtime(now)
now_local_str = " ".join(map(str, now_local))

print(now_local)
print(now_local_str)

oled.fill(0)
oled.text('last now:',0,0,1)
oled.text(now_local_str,0,16,1)
oled.show()
time.sleep(1)

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
    print(timestamp)
    timestamp_local = time.localtime(timestamp)
    timestamp_local_str = " ".join(map(str, timestamp_local))
    print(timestamp_local_str)
    oled.fill(0)
    oled.text('next:',0,0,1)
    oled.text(planetname,0,16,1)
    oled.text(action,64,16,1)
    oled.text(timestamp_local_str,0,32,1)
    oled.text(str(timestamp - now),0,48,1)
    oled.show()

    # sleep until timestamp
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
