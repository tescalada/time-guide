import gc

import network
import ssd1306
import urequests as requests
import gfx
import math
import utime
import umatrix as matrix
import ulinalg as linalg

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

visible_i = [0, 0, 0, 0, 0, 0, 0]  # currently above horizon
alc_i = [0, 0, 0, 0, 0, 0, 0]  # current altitude
alm_i = [0, 0, 0, 0, 0, 0, 0]  # maximum altitude
azc_i = [0, 0, 0, 0, 0, 0, 0]  # current azimuth
azr_i = [0, 0, 0, 0, 0, 0, 0]  # azimuth at planet rise
azs_i = [0, 0, 0, 0, 0, 0, 0]  # aximuth at planet set
azm_i = [0, 0, 0, 0, 0, 0, 0]  # azimuth at maximum altitude

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

        # sky chart data
        # obtain current planet azimuth from wolframalpha API
        url = "http://api.wolframalpha.com/v1/result?i={0}%20azimuth%3F&appid={1}".format(name, WOLFRAM_API_KEY)
        r = requests.get(url)
        print(r.text)
        azc = [x.strip() for x in r.text.split(',')]
        azc = [x.strip() for x in azc[0].split()]
        azc = azc[0]
        azc = float(azc)
        print(azc)
        r.close()
        del r
        gc.collect()
        # save planet data to list
        azc_i[index] = azc

        # obtain planet azimuth rise from wolframalpha API
        url = "http://api.wolframalpha.com/v1/result?i={0}%20azimuth%20rise%3F&appid={1}".format(name, WOLFRAM_API_KEY)
        r = requests.get(url)
        print(r.text)
        azr = [x.strip() for x in r.text.split(',')]
        azr = [x.strip() for x in azr[0].split()]
        azr = azr[0]
        azr = float(azr)
        print(azr)
        r.close()
        del r
        gc.collect()
        # save planet data to list
        azr_i[index] = azr

        # obtain planet azimuth set from wolframalpha API
        url = "http://api.wolframalpha.com/v1/result?i={0}%20azimuth%20set%3F&appid={1}".format(name, WOLFRAM_API_KEY)
        r = requests.get(url)
        print(r.text)
        azs = [x.strip() for x in r.text.split(',')]
        azs = [x.strip() for x in azs[0].split()]
        azs = azs[0]
        azs = float(azs)
        print(azs)
        r.close()
        del r
        gc.collect()
        # save planet data to list
        azs_i[index] = azs

        # obtain planet azimuth at maximum altitude from wolframalpha API
        url = "http://api.wolframalpha.com/v1/result?i={0}%20azimuth%20at%20time%20of%20maximum%20altitude%3F&appid={1}".format(name, WOLFRAM_API_KEY)
        r = requests.get(url)
        print(r.text)
        azm = [x.strip() for x in r.text.split(',')]
        azm = [x.strip() for x in azm[0].split()]
        azm = azm[0]
        azm = float(azm)
        print(azm)
        r.close()
        del r
        gc.collect()
        # save planet data to list
        azm_i[index] = azm

        # obtain current planet altitude from wolframalpha API
        url = "http://api.wolframalpha.com/v1/result?i={0}%20altitude%3F&appid={1}".format(name, WOLFRAM_API_KEY)
        r = requests.get(url)
        print(r.text)
        alc = [x.strip() for x in r.text.split(',')]
        alc = [x.strip() for x in alc[0].split()]
        alc = alc[0]
        alc = float(alc)
        print(alc)
        r.close()
        del r
        gc.collect()
        # save planet data to list
        alc_i[index] = alc

        # obtain max planet altitude from wolframalpha API
        url = "http://api.wolframalpha.com/v1/result?i={0}%20maximum%20altitude%3F&appid={1}".format(name, WOLFRAM_API_KEY)
        r = requests.get(url)
        print(r.text)
        alm = [x.strip() for x in r.text.split(',')]
        alm = [x.strip() for x in alm[0].split()]
        alm = alm[0]
        alm = float(alm)
        print(alm)
        r.close()
        del r
        gc.collect()
        # save planet data to list
        alm_i[index] = alm

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

        # sky chart
        xc = 94
        yc = 31
        rad = 29
        graphics.circle(xc, yc, rad, 1)

        # show planet rise azimuth
        x = int(round(rad * math.cos(math.radians(azr_i[index] - 90)),0))
        y = int(round(rad * math.sin(math.radians(azr_i[index] - 90)),0))
        xr = xc + x
        yr = yc + y
        graphics.fill_circle(xr, yr, 2, 1)

        # show planet set azimuth
        x = int(round(rad * math.cos(math.radians(azs_i[index] - 90)),0))
        y = int(round(rad * math.sin(math.radians(azs_i[index] - 90)),0))
        xs = xc + x
        ys = yc + y
        graphics.fill_circle(xs, ys, 2, 1)

        # show location at maximum altitude
        rd = int(round(rad * math.cos(math.radians(alm_i[index])),0))
        x = int(round(rd * math.cos(math.radians(azm_i[index] - 90)),0))
        y = int(round(rd * math.sin(math.radians(azm_i[index] - 90)),0))
        xm = xc + x
        ym = yc + y
        graphics.fill_circle(xm, ym, 2, 1)

        # show current location if visible
        if visible_i[index] == 'Yes':
            rd = int(round(rad * math.cos(math.radians(alc_i[index])),0))
            x = int(round(rd * math.cos(math.radians(azc_i[index] - 90)),0))
            y = int(round(rd * math.sin(math.radians(azc_i[index] - 90)),0))
            xcu = xc + x
            ycu = yc + y
            graphics.circle(xcu, ycu, 2, 1)

        # find path of transit
        A = matrix.matrix([[xr ** 2, xr, 1], [xm ** 2, xm, 1], [xs ** 2, xs, 1]])
        B = matrix.matrix([[yr], [ym], [ys]])
        d_i = linalg.det_inv(A)
        invA = d_i[1]
        X = linalg.dot(invA, B)

        for i in range(xr - xs):
            x = xs + i
            oled.pixel(x, yc - int((X[0] * x ** 2)) + int((X[1] * x)) + int(X[2]), 1)

        oled.show()
        utime.sleep(10)

    # collect garbage just in case that is causing the crashes
    gc.collect()