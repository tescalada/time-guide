import gc

import network
import ssd1306
import urequests as requests
import gfx
import math
import utime

#from rotary_irq_esp import RotaryIRQ
from machine import I2C, Pin

from credentials import WIFI_SSID, WIFI_PASSWORD, WOLFRAM_API_KEY

oled_reset_pin = Pin(16, Pin.OUT)
oled_reset_pin.value(1)

utime.sleep(1)

i2c = I2C(scl=Pin(15), sda=Pin(4))

oled = ssd1306.SSD1306_I2C(128, 64, i2c)
utime.sleep(1)

graphics = gfx.GFX(128, 64, oled.pixel)

oled.fill(0)
oled.text('oled init',0,0,1)
oled.show()
utime.sleep(1)

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

oled.fill(0)
oled.text('wifi connected',0,0,1)
oled.show()
utime.sleep(1)

names = ['Mercury', 'Venus', 'Mars', 'Jupiter', 'Saturn', 'Uranus', 'Neptune']

visible_i = [0, 0, 0, 0, 0, 0, 0]
al_i = [0, 0, 0, 0, 0, 0, 0]
az_i = [0, 0, 0, 0, 0, 0, 0]

oled.fill(0)
oled.text('begin loop',0,0,1)
oled.show()
utime.sleep(1)

while True:
    for index, name in enumerate(names):
        #oled stuff
        oled.fill(0)
        oled.text("getting:", 0, 0)
        oled.text(name, 0, 10)
        oled.show()
        utime.sleep(1)

        # obtain planet above horizon from wolframalpha API
        url = "http://api.wolframalpha.com/v1/result?i={0}%20above%20horizon%3F&appid={1}".format(name, WOLFRAM_API_KEY)
        r = requests.get(url)
        print(r.text)
        visible = [x.strip() for x in r.text.split(',')]
        visible = visible[0]
        print(visible)
        r.close()
        del r
        gc.collect()
        # save planet data to list
        visible_i[index] = visible

        # obtain planet altitude from wolframalpha API
        url = "http://api.wolframalpha.com/v1/result?i={0}%20altitude%3F&appid={1}".format(name, WOLFRAM_API_KEY)
        r = requests.get(url)
        print(r.text)
        al = [x.strip() for x in r.text.split(',')]
        al = [x.strip() for x in al[0].split()]
        al = al[0]
        al = float(al)
        print(al)
        r.close()
        del r
        gc.collect()
        # save planet data to list
        al_i[index] = al

        # obtain planet azimuth from wolframalpha API
        url = "http://api.wolframalpha.com/v1/result?i={0}%20azimuth%3F&appid={1}".format(name, WOLFRAM_API_KEY)
        r = requests.get(url)
        print(r.text)
        az = [x.strip() for x in r.text.split(',')]
        az = [x.strip() for x in az[0].split()]
        az = az[0]
        az = float(az)
        print(az)
        r.close()
        del r
        gc.collect()
        # save planet data to list
        az_i[index] = az

        #oled stuff
        oled.fill(0)
        oled.text(name, 0, 0)
        oled.text("acquired!", 0, 10)
        oled.show()
        utime.sleep(1)

    for index, name in enumerate(names):
        oled.fill(0)
        oled.show()

        # display stuff
        oled.text(name, 0, 0)
        oled.text("Visible:", 0,10)
        oled.text(visible_i[index], 80,10)
        oled.show()

        # show planet altitude
        if visible_i[index] == 'Yes':
            oled.line(0, 48, 18, 48, 1)
            y = 18 * math.sin(math.radians(al_i[index]))
            y = int(round(y,0))
            oled.line(0, 48, 18, 48 - y, 1)
            oled.text(str(round(al_i[index])), 22, 42)

        # show planet azimuth
        xc = 80
        yc = 48
        rad = 10
        oled.text("N", xc - 3, 30)
        oled.text(str(round(az_i[index])), xc + 15, 42)
        graphics.circle(xc, yc, rad, 1)
        x = rad * math.cos(math.radians(az_i[index] - 90))
        x = round(x,0)
        y = rad * math.sin(math.radians(az_i[index] - 90))
        y = round(y,0)
        oled.line(xc, yc, int(xc + x), int(yc + y), 1)
        oled.show()

        utime.sleep(10)

        oled.fill(0)
        oled.show()

    # collect garbage just in case that is causing the crashes
    gc.collect()