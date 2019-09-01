import gc

import ssd1306
import sh1106
import gfx
import math
import utime
#import network

from machine import I2C, Pin, SPI

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

long_i = [200.0, 48.0, 126.0, 260.0, 286.0, 33.0, 346.0]
years_i = ['August 20, 2019', 'August 8, 2019', 'August 3, 2020', 'January 24, 2023', 'December 24, 2032', 'February 10, 2051', 'July 16, 2047']
longp_i = [76.0, 131.0, 336.0, 14.0, 93.0, 173.0, 49.0]
period_i = [0.2408467, 0.61519726, 1.8808476, 11.862615, 29.447498, 84.016846, 164.79132]
dist_i = [0.928, 1.65, 2.51, 4.29, 9.1, 20.5, 29.8]
sdist_i = [0.417, 0.723, 1.64, 5.3, 10.1, 19.8, 29.9]
elong = 0
names = ['Mercury', 'Venus', 'Mars', 'Jupiter', 'Saturn', 'Uranus', 'Neptune']

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


def orbitTracker(name):
    # graphics on display
    # calculate progress towards perihelion
    # orbit progress circle dims
    xc = 94
    yc = 31
    rad = int(pxc[names.index(name)]/4)

    #draw orbit progress circle outline
    graphics2.circle(xc, yc, rad, 1)

    #calculate orbit progress in radians
    p_rad = math.radians(long_i[names.index(name)])
    print(p_rad)

    #calculate x,y position of planet in heliocentric coordinates relative to xc,yc
    xp = int(round(rad * math.cos(p_rad),0))
    yp = int(round(rad * math.sin(p_rad),0))

    #draw rectangle blocks and planet marker
    xblock = int(math.fabs(xp))

    # top-right
    if p_rad <= math.pi/2:
        #fill bottom half of circle
        graphics2.fill_rect(xc - rad, yc, 2 * rad + 1, rad + 1, 0)
        #fill top left of circle
        graphics2.fill_rect(xc - rad, yc - rad, rad + 1, rad + 1, 0)
        #partial fill top right of circle
        graphics2.fill_rect(xc, yc - rad, xblock + 1, rad + 1, 0)

    # top-left
    elif p_rad >= math.pi/2 and p_rad <= math.pi:
       #fill bottom half of circle
        graphics2.fill_rect(xc - rad, yc, 2 * rad + 1, rad + 1, 0)
        #partial fill top left of circle
        graphics2.fill_rect(xc - rad, yc - rad, rad - xblock, rad + 1, 0)

    # bottom left
    elif p_rad >= math.pi and p_rad <= 3 * math.pi/2:
       #fill bottom right of circle
        graphics2.fill_rect(xc, yc, rad + 1, rad + 1, 0)
        #partial fill bottom left of circle
        graphics2.fill_rect(xc - xblock, yc, xblock + 1, rad + 1, 0)

    # bottom-right
    else:
        #partial fill bottom right of circle
        graphics2.fill_rect(xc + xblock, yc, rad - xblock + 1, rad + 1, 0)

    # plot planet marker
    graphics2.circle(xc + xp, yc - yp, pr[names.index(name)], 1)
    graphics2.fill_circle(xc + xp, yc - yp, 1, 1)

    # plot earth
    xe = int(round((sdist_i[2]/4) * math.cos(elong),0))
    ye = int(round((sdist_i[2]/4) * math.sin(elong),0))
    graphics2.circle(xc + xe, yc - ye, 1, 1)

#        # plot earth - planet distance
#        display.line(xc + xp, yc + yp, xc + xe, yc + ye, 1)

    # make sun
    graphics2.fill_circle(xc, yc, 2, 1)

    # show perihelion location
    longp = longp_i[names.index(name)]
    longp = math.radians(longp)
    xpp = int((rad) * math.cos(longp))
    ypp = int((rad) * math.sin(longp))
    graphics2.line(xc, yc, xc + xpp, yc + ypp, 1)

    display2.text(name, 0, 0)
    display2.show()


    # show data on display1
    display1.text(name, 0, 0)
    display1.text('Heliocent. long.: ',0,15)
    display1.text(str(int(long_i[names.index(name)])),0,25)
    display1.text('D to Earth (AU): ',0,38)
    display1.text(str(round(dist_i[names.index(name)],1)),0,48)

    display1.show()
    utime.sleep(10)

    display1.fill(0)
    display1.text(name, 0, 0)
    display1.text('Next perihelion:',0,15)
    display1.text(years_i[names.index(name)],0,25)
    display1.text('Orbital pd (yr):',0,38)
    display1.text(str(round(period_i[names.index(name)],1)),0,48)
    display1.show()

    # collect garbage just in case that is causing the crashes
    gc.collect()