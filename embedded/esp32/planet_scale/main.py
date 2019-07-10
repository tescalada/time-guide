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

i2c = I2C(scl=Pin(15), sda=Pin(4))

oled = ssd1306.SSD1306_I2C(128, 64, i2c)
utime.sleep(1)

graphics = gfx.GFX(128, 32, oled.pixel)

oled.fill(0)
oled.text('oled init',0,0,1)
oled.show()
utime.sleep(2)

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
utime.sleep(2)

dist_i = [0, 0, 0, 0, 0, 0, 0]
sdist_i = [0, 0, 0, 0, 0, 0, 0]

names = ['Mercury', 'Venus', 'Mars', 'Jupiter', 'Saturn', 'Uranus', 'Neptune']

oled.fill(0)
oled.text('begin loop',0,0,1)
oled.show()
utime.sleep(1)

while True:
   #oled stuff
   # make log10 orbit distances

    url = "http://api.wolframalpha.com/v1/result?i=earth%20distance%20from%20sun%3F&appid={0}".format(WOLFRAM_API_KEY)
    r = requests.get(url)
    print(r.text)
    esdist = [x.strip() for x in r.text.split(',')]
    esdist = [x.strip() for x in esdist[0].split()]
    esdist = esdist[1]
    r.close()
    del r
    esdist = float(esdist)
    sdist_i.insert(2, esdist)

    # create log scale of sizes of planets
    arb = 0.9
    pre = [1, 2.48, 2.61, 1.39, 28.66, 23.9, 10.4, 10.1]
    pre.insert(0, arb)
    scale = 3.5
    pre = [scale * math.log(x/pre[0],10) for x in pre]
    pre.pop(0)
    pre = [int(math.ceil(x)) for x in pre]

    # size of planets without earth
    pr = list.copy(pre)
    pr.pop(2)

    for index, name in enumerate(names):
        # oled stuff
        oled.fill(0)
        oled.text("getting:", 0, 0)
        oled.text(name, 0, 10)
        oled.show()
        utime.sleep(2)

         # distance from sun
        url = "http://api.wolframalpha.com/v1/result?i={0}%20distance%20from%20sun%3F&appid={1}".format(name, WOLFRAM_API_KEY)
        r = requests.get(url)
        print(r.text)
        sdist = [x.strip() for x in r.text.split(',')]
        sdist = [x.strip() for x in sdist[0].split()]
        sdist = sdist[1]
        r.close()
        del r
        print(sdist)
        # save planet data to list
        sdist_i[index] = float(sdist)

        gc.collect()

        #oled stuff
        oled.fill(0)
        oled.text(name, 0, 0)
        oled.text("acquired!", 0, 10)
        oled.show()
        utime.sleep(2)

    for index, name in enumerate(names):
        # create log scale of distances of planets from sun
        arb = 0.2
        sdist_i.insert(0, arb)
        scale = 57
        sdist_i = [scale * math.log(x/sdist_i[0],10) for x in sdist_i]
        sdist_i.pop(0)
        sdist_i = [int(math.ceil(x)) for x in sdist_i]

        # distances of planets without earth
        pxc = list.copy(sdist_i)
        pxc.pop(2)

        oled.fill(0)
        oled.show()

        #show planet index graphic
        graphics.circle(sdist_i[0], 16, pre[0], 1)
        graphics.circle(sdist_i[1], 16, pre[1], 1)
        graphics.fill_circle(sdist_i[2], 16, pre[2], 1)
        graphics.circle(sdist_i[3], 16, pre[3], 1)
        graphics.circle(sdist_i[4], 16, pre[4], 1)
        graphics.circle(sdist_i[5], 16, pre[5], 1)
        graphics.circle(sdist_i[6], 16, pre[6], 1)
        graphics.circle(sdist_i[7], 16, pre[7], 1)

        oled.line(pxc[index]-pr[index], 31, pxc[index]+pr[index], 31, 1)
        oled.show()
        utime.sleep(2)


    # collect garbage just in case that is causing the crashes
    gc.collect()