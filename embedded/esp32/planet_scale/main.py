import gc

import ssd1306
import sh1106
import gfx
import math
import utime
import network
from rotary_irq_esp import RotaryIRQ
#from shapes3d import sphere
from planetFn import orbitTracker, skyChart, skyLocation, initStar, showStarfield
from credentials import WIFI_SSID, WIFI_PASSWORD, WOLFRAM_API_KEY
import urequests as requests
from scron.week import simple_cron

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

def orbit_loc_all():
    for index, name in enumerate (names_e):
        #heliocentric longitude
        url = "http://api.wolframalpha.com/v1/result?i={0}%20heliocentric%20longitude%3F&appid={1}".format(name, WOLFRAM_API_KEY)
        r = requests.get(url)
        print(r.text)
        long = [x.strip() for x in r.text.split(',')]
        long = [x.strip() for x in long[0].split()]
        long = long[0]
        r.close()
        del r
        print(long)
        long = int(long)

        xp[index] = int(rad_i[index] * math.cos(math.radians(long)))
        yp[index] = int(rad_i[index] * math.sin(math.radians(long)))

    for index, name in enumerate (names):
        # obtain planet above horizon from wolframalpha API
        url = "http://api.wolframalpha.com/v1/result?i={0}%20above%20horizon%3F&appid={1}".format(name, WOLFRAM_API_KEY)
        r = requests.get(url)
        print(r.text)
        visible[index] = [x.strip() for x in r.text.split(',')]
        visible[index] = visible[index][0]
        print(visible[index])
        r.close()
        del r
        gc.collect()

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

        # calculate current location if visible
        rad = 29

        if visible[index] == 'Yes':
            rd = int(round(rad * (90 - alc)/90,0))
            x = int(round(rd * math.cos(math.radians(azc - 90)),0))
            y = int(round(rd * math.sin(math.radians(azc - 90)),0))
            xcu[index] = xcp + x
            ycu[index] = ycp + y


#define planet menu parameters
names = ['Mercury', 'Venus', 'Mars', 'Jupiter', 'Saturn', 'Uranus', 'Neptune']
names_e = ['Mercury', 'Venus', 'Mars', 'Earth', 'Jupiter', 'Saturn', 'Uranus', 'Neptune']
xp = [0, 0, 0, 0, 0, 0, 0, 0]
yp = [0, 0, 0, 0, 0, 0, 0, 0]
visible = [0, 0, 0, 0, 0, 0, 0]
xcu = [0, 0, 0, 0, 0, 0, 0]
ycu = [0, 0, 0, 0, 0, 0, 0]
xcp = 35
ycp = 31

menu = ['Planet Menu', 'Sky Chart', 'Sky Location', 'Orbital Data']
# log scale of sizes of planets
pre = [1, 2, 2, 1, 6, 5, 4, 4]
# size of planets without earth
pr =  [1, 2, 1, 6, 5, 4, 4]

# create log scale of distances of planets from sun
sdist_i = [20, 31, 40, 52, 81, 96, 113, 123]
pxc = [20, 31, 52, 81, 96, 113, 123]
rad_i = [5, 7, 10, 13, 20, 24, 28, 30]

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

simple_cron.run()
# orbitTracker_all needs to be cached 1/day
simple_cron.add(
    'Hourly',
    lambda *a,**k: orbit_loc_all(),
    minutes=range(0, 59, 2),
    seconds=0
)

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

        #Perihelion all orbits display
        display1.text('P', 92, 0, 1)
        letter = ['M', 'V', 'E', 'M', 'J', 'S', 'U', 'N']
        let_dispy = [10, 20, 30, 40, 10, 20, 30, 40]
        let_dispx = [75, 75, 75, 75, 110, 110, 110, 110]
        #draw orbits
        for index in range(len(names_e)):
            graphics1.circle(xcp, ycp, rad_i[index], 1)
            graphics1.circle(xcp + xp[index], ycp - yp[index], pre[index], 1)
            graphics1.fill_circle(xcp + xp[index], ycp - yp[index], 1, 1)
            display1.text(letter[index], let_dispx[index], let_dispy[index], 1)
            display1.show()

        #Sky location all planet display
        display2.text('V', 92, 0, 1)
        letter.pop(2)
        let_dispx.pop(2)
        let_dispy.pop(2)
        rad = 29
        #Visible on sky location display
        for index in range(len(names)):
            graphics2.circle(xcp, ycp, rad, 1)
            if visible[index] == 'Yes':
                graphics2.circle(xcu[index], ycu[index], 2, 1)
                graphics2.fill_rect(let_dispx[index]-1, let_dispy[index]-1, 10, 10, 1)
                display2.text(letter[index], let_dispx[index], let_dispy[index], 0)
            else:
                display2.text(letter[index], let_dispx[index], let_dispy[index], 1)
            display2.show()

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
                            display1.fill(0)
                            display2.fill(0)
                            display1.show()
                            display2.show()
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
                            val2 = r2.value()
                            if lastval2 != val2:
                                    display1.fill(0)
                                    display2.fill(0)
                                    display1.show()
                                    display2.show()
                                    break

                        elif menufn == 'Sky Location':
                            skyLocation(name)
                            val2 = r2.value()
                            if lastval2 != val2:
                                    display1.fill(0)
                                    display2.fill(0)
                                    display1.show()
                                    display2.show()
                                    break

                        elif menufn == 'Orbital Data':
                            orbitTracker(name)
                            val2 = r2.value()
                            if lastval2 != val2:
                                    display1.fill(0)
                                    display2.fill(0)
                                    display1.show()
                                    display2.show()
                                    break

#                        elif menufn == 'Orbit 3d':
#                            display2.fill(0)
#                            display2.show()
#                            n = 0
#                            while n >= 0:
#                                rad = 30
#                                xc = int(65 + 50 * math.sin(n))
#                                yc = int(33 + 20 * math.sin(n))
#                                f = int(121 + 120 * math.cos(n))
#                                xr = 0
#                                yr = int(n * 25)
#                                zr = 23
#                                sphere(rad, xc, yc, f, xr, yr, zr)
#                                n += 0.25
#                                val2 = r2.value()
#                                if lastval2 != val2:
#                                    display1.fill(0)
#                                    display2.fill(0)
#                                    display1.show()
#                                    display2.show()
#                                    break

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