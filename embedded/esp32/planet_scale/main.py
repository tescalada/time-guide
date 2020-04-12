import gc

import ssd1306
import sh1106
import gfx
import math
import utime
import network
from rotary_irq_esp import RotaryIRQ
from planetFn import orbitTracker, skyChart, skyLocation, initStar, showStarfield
from credentials import WIFI_SSID, WIFI_PASSWORD

from machine import I2C, Pin, SPI

button = Pin(27, Pin.IN, Pin.PULL_UP)

oled_reset_pin = Pin(16, Pin.OUT)

hspi = SPI(1, 10000000, sck=Pin(18), mosi=Pin(23), miso=Pin(19))

display1 = sh1106.SH1106_SPI(128, 64, hspi, dc=Pin(26), res=oled_reset_pin, cs=Pin(5))
display2 = sh1106.SH1106_SPI(128, 64, hspi, dc=Pin(33), res=oled_reset_pin, cs=Pin(2))

utime.sleep(1)

display1.sleep(False)
display1.rotate(1)
display2.sleep(False)
display2.rotate(1)
utime.sleep(1)

i2c = I2C(scl=Pin(15), sda=Pin(4))

oled = ssd1306.SSD1306_I2C(128, 64, i2c)
utime.sleep(1)

graphics = gfx.GFX(128, 64, oled.pixel)
graphics1 = gfx.GFX(128, 64, display1.pixel)
graphics2 = gfx.GFX(128, 64, display2.pixel)

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


oled.fill(0)
oled.text('oled init',0,0,1)
oled.show()

display1.fill(0)
display1.text('display init',0,0,1)
graphics1.circle(63, 32, 10, 1)

display2.fill(0)
display2.text('display2 init',0,0,1)
graphics2.circle(63, 32, 10, 1)

display1.show()
display2.show()

utime.sleep(1)

def planetMenu():
    global lastval

    oled.fill(0)

    # make huge sun
    oled.vline(0, 0, 64, 1)
    oled.vline(1, 0, 64, 1)
    oled.vline(2, 0, 64, 1)
    oled.vline(3, 0, 64, 1)
    oled.vline(4, 0, 64, 1)
    oled.vline(5, 0, 64, 1)
    oled.vline(6, 0, 64, 1)
    oled.vline(7, 0, 64, 1)
    oled.vline(8, 3, 58, 1)
    oled.vline(9, 16, 33, 1)
    oled.vline(10, 23, 19, 1)

    # show planet index graphic
    graphics.circle(sdist_i[0], 31, pre[0], 1)
    graphics.circle(sdist_i[1], 31, pre[1], 1)
    graphics.fill_circle(sdist_i[2], 31, pre[2], 1)
    graphics.circle(sdist_i[3], 31, pre[3], 1)
    graphics.circle(sdist_i[4], 31, pre[4], 1)
    graphics.circle(sdist_i[5], 31, pre[5], 1)
    oled.line(sdist_i[5] - pre[5], 37, sdist_i[5] + pre[5], 25, 1)
    graphics.circle(sdist_i[6], 31, pre[6], 1)
    graphics.circle(sdist_i[7], 31, pre[7], 1)

    val = r.value()
    if lastval != val:
        lastval = val
        print('result =', val)
        oled.text(names[val], 16, 0, 1)
        oled.line(pxc[val]-pr[val], 41, pxc[val]+pr[val], 41, 1)
        oled.show()

    utime.sleep_ms(50)

#define planet menu parameters
names = ['Mercury', 'Venus', 'Mars', 'Jupiter', 'Saturn', 'Uranus', 'Neptune']
menu = ['Planet Menu', 'Sky Location', 'Sky Chart', 'Orbital Data']

sdist_i = [0.417, 0.723, 1.64, 5.3, 10.1, 19.8, 29.9]

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

# create log scale of distances of planets from sun
arb = 0.2
sdist_i = [0.466, 0.72, 1.02, 1.66, 5.29, 10, 19.8, 29.9]
sdist_i.insert(0, arb)
scale = 57
sdist_i = [scale * math.log(x/sdist_i[0],10) - 1 for x in sdist_i]
sdist_i.pop(0)
sdist_i = [int(math.ceil(x)) for x in sdist_i]

# distances of planets from sun without earth
pxc = list.copy(sdist_i)
pxc.pop(2)


oled.fill(0)
display1.fill(0)
display2.fill(0)

oled.show()
display1.show()
display2.show()


# define rotary variables
r = RotaryIRQ(pin_num_clk=14,
      pin_num_dt=13,
      min_val=0,
      max_val=len(names)-1,
      reverse=True,
      range_mode=RotaryIRQ.RANGE_WRAP)

lastval = r.value()


#define starfield screensaver variables
stars = 500
star_x = list(range(stars))
star_y = list(range(stars))
star_z = list(range(stars))
xc = 63
yc = 31


for i in range(stars):
    initStar(i, star_x, star_y, star_z)

while True:
    showStarfield(stars, star_x, star_y, star_z, xc, yc)

    if not button.value():
        print('Planet button pressed!')
        oled.fill(0)
        display1.fill(0)
        display2.fill(0)
        oled.show()
        display1.show()
        display2.show()
        utime.sleep_ms(250)

        # make huge sun
        oled.vline(0, 0, 64, 1)
        oled.vline(1, 0, 64, 1)
        oled.vline(2, 0, 64, 1)
        oled.vline(3, 0, 64, 1)
        oled.vline(4, 0, 64, 1)
        oled.vline(5, 0, 64, 1)
        oled.vline(6, 0, 64, 1)
        oled.vline(7, 0, 64, 1)
        oled.vline(8, 3, 58, 1)
        oled.vline(9, 16, 33, 1)
        oled.vline(10, 23, 19, 1)

        # show planet index graphic
        graphics.circle(sdist_i[0], 31, pre[0], 1)
        oled.line(pxc[0]-pr[0], 41, pxc[0]+pr[0], 41, 1)
        oled.text(names[0], 16, 0, 1)
        graphics.circle(sdist_i[1], 31, pre[1], 1)
        graphics.fill_circle(sdist_i[2], 31, pre[2], 1)
        graphics.circle(sdist_i[3], 31, pre[3], 1)
        graphics.circle(sdist_i[4], 31, pre[4], 1)
        graphics.circle(sdist_i[5], 31, pre[5], 1)
        oled.line(sdist_i[5] - pre[5], 37, sdist_i[5] + pre[5], 25, 1)
        graphics.circle(sdist_i[6], 31, pre[6], 1)
        graphics.circle(sdist_i[7], 31, pre[7], 1)
        oled.show()

        while True:

            planetMenu()

            if not button.value():
                print('Planet button pressed!')
                r2 = RotaryIRQ(pin_num_clk=14,
                              pin_num_dt=13,
                              min_val=0,
                              max_val=len(menu)-1,
                              reverse=True,
                              range_mode=RotaryIRQ.RANGE_WRAP)
                lastval2 = r2.value()
                utime.sleep_ms(250)
                oled.fill(0)
                oled.text('Function menu', 0, 0, 1)
                oled.hline(0, 12, 128, 1)
                oled.show()

                while True:
                    if not button.value():
                        print('Menu button pressed!')
                        utime.sleep_ms(250)
                        name = names[lastval]
                        menufn = menu[lastval2]
                        print(name)
                        print(menufn)

                        if menufn == 'Planet Menu':
                            oled.fill(0)
                            oled.show()
                            r = RotaryIRQ(pin_num_clk=14,
                                    pin_num_dt=13,
                                    min_val=0,
                                    max_val=len(names)-1,
                                    reverse=True,
                                    range_mode=RotaryIRQ.RANGE_WRAP)
                            lastval = r.value()
                            break

                        elif menufn == 'Sky Chart':
                            skyChart(name)

                        elif menufn == 'Sky Location':
                            skyLocation(name)

                        elif menufn == 'Orbital Data':
                            orbitTracker(name)

                    val2 = r2.value()
                    if lastval2 != val2:
                        lastval2 = val2
                        print('result2 =', val2)
                        oled.fill(0)
                        oled.text(menu[val2], 0, 0, 1)
                        oled.show()
                    utime.sleep_ms(50)


            # collect garbage just in case that is causing the crashes
            gc.collect()