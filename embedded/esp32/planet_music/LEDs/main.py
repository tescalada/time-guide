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
oled_i2c = I2C(scl=Pin(15), sda=Pin(4))
time.sleep(1)
oled = ssd1306.SSD1306_I2C(128, 64, oled_i2c)
time.sleep(1)
graphics = gfx.GFX(128, 64, oled.pixel)
time.sleep(1)

# define variables
names = ['Sun', 'Moon', 'Mercury', 'Venus', 'Mars', 'Jupiter', 'Saturn', 'Uranus', 'Neptune']

#initialize neopixel
n = 81
p = 13
np = neopixel.NeoPixel(machine.Pin(p), n, bpp=4)

def do_connect():
    wlan = network.WLAN(network.STA_IF)
    # wlan.config(dhcp_hostname = 'planet_chimes')
    wlan.active(True)
    if not wlan.isconnected():
        wlan.config(dhcp_hostname="esp32-planet-chimes")
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

        oled.fill(0)
        oled.text('acquired:',0,0,1)
        oled.text(name,0,16,1)
        oled.show()

    rise = [tuple(l) for l in rise]
    sett = [tuple(l) for l in sett]
    planet_list = rise + sett
    return planet_list


# LED list for each light
LED = [(0, 0, 0, 25),
       (0, 0, 0, 50),
       (0, 0, 0, 75),
       (0, 0, 0, 100),
       (0, 0, 0, 125),
       (0, 0, 0, 150),
       (0, 0, 0, 175),
       (0, 0, 0, 200),
       (0, 0, 0, 225)]

# set the RTC
def set_time_with_retry(retries):
    while True:
        if retries == 0:
            return
        try:
            settime()
            print('settime successful')
            oled.fill(0)
            oled.text('settime successful',0,0,1)
            oled.show()
            time.sleep(1)
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

for i in range(len(names)):
    #clear LEDs at boot
    np[i * 9] = (0, 0, 0, 0)
    np[i * 9 + 1] = (0, 0, 0, 0)
    np[i * 9 + 2] = (0, 0, 0, 0)
    np[i * 9 + 3] = (0, 0, 0, 0)
    np[i * 9 + 4] = (0, 0, 0, 0)
    np[i * 9 + 5] = (0, 0, 0, 0)
    np[i * 9 + 6] = (0, 0, 0, 0)
    np[i * 9 + 7] = (0, 0, 0, 0)
    np[i * 9 + 8] = (0, 0, 0, 0)
    np.write()
    time.sleep(0.5)

    #turn on LEDs for planets already above horizon
    if planet_list[i][0] > planet_list[i + 9][0]:
        np[i * 9] = LED[0]
        np[i * 9 + 1] = LED[1]
        np[i * 9 + 2] = LED[2]
        np[i * 9 + 3] = LED[3]
        np[i * 9 + 4] = LED[4]
        np[i * 9 + 5] = LED[5]
        np[i * 9 + 6] = LED[6]
        np[i * 9 + 7] = LED[7]
        np[i * 9 + 8] = LED[8]
        np.write()
        print(planet_list[i][1])
        print('above horizon')

list.sort(planet_list)

while True:
    timestamp, planetname, action = planet_list.pop(0)
    print(timestamp)
    timestamp_local = time.localtime(timestamp)
    timestamp_local_str = " ".join(map(str, timestamp_local))
    print(timestamp_local_str)

    delay = timestamp - now

    if delay > 0:

        oled.fill(0)
        oled.text('next',0,0,1)
        oled.text(planetname,35,0,1)
        oled.text(action,95,0,1)
        oled.text(timestamp_local_str,0,10,1)
        oled.text('last now:',0,20,1)
        oled.text(now_local_str,0,30,1)
        oled.text('sleep:',0,40,1)
        oled.text(str(delay),0,50,1)
        oled.text('secs',95,50,1)
        oled.show()

        # sleep until timestamp
        time.sleep(delay)

    planet_num = names.index(planetname)
    if action == "rise":
        np[planet_num * 9] = LED[0]
        np[planet_num * 9 + 1] = LED[1]
        np[planet_num * 9 + 2] = LED[2]
        np[planet_num * 9 + 3] = LED[3]
        np[planet_num * 9 + 4] = LED[4]
        np[planet_num * 9 + 5] = LED[5]
        np[planet_num * 9 + 6] = LED[6]
        np[planet_num * 9 + 7] = LED[7]
        np[planet_num * 9 + 8] = LED[8]
        np.write()
        print(planetname)
        print('rise')

        next_timestamp = planet_timestamp(planetname, 'rise')
        next_tuple = (next_timestamp, planetname, 'rise')

    elif action == "sett":
        np[planet_num * 9] = (0, 0, 0, 0)
        np[planet_num * 9 + 1] = (0, 0, 0, 0)
        np[planet_num * 9 + 2] = (0, 0, 0, 0)
        np[planet_num * 9 + 3] = (0, 0, 0, 0)
        np[planet_num * 9 + 4] = (0, 0, 0, 0)
        np[planet_num * 9 + 5] = (0, 0, 0, 0)
        np[planet_num * 9 + 6] = (0, 0, 0, 0)
        np[planet_num * 9 + 7] = (0, 0, 0, 0)
        np[planet_num * 9 + 8] = (0, 0, 0, 0)
        np.write()
        print(planetname)
        print('set')

        next_timestamp = planet_timestamp(planetname, 'set')
        next_tuple = (next_timestamp, planetname, 'sett')

    set_time_with_retry(3)

    now = int(time.time()) # return time since the Epoch (embedded)
    print(now)
    now_local = time.localtime(now)
    now_local_str = " ".join(map(str, now_local))
    print(now_local_str)

    planet_list.append(next_tuple)
    list.sort(planet_list)
