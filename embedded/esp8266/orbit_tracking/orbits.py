import gc

import network
import ssd1306
import sh1106
import urequests as requests
import gfx
import math
import utime

#from rotary_irq_esp import RotaryIRQ
from machine import I2C, Pin, SPI

oled_reset_pin = Pin(16, Pin.OUT)

spi = SPI(1, baudrate=800000)

display = sh1106.SH1106_SPI(128, 64, spi, dc=Pin(0), res=oled_reset_pin, cs=Pin(15))
utime.sleep(1)

display2 = sh1106.SH1106_SPI(128, 64, spi, dc=Pin(2), res=oled_reset_pin, cs=Pin(1))
utime.sleep(1)

display.sleep(False)
display.rotate(1)
utime.sleep(1)

display2.sleep(False)
display2.rotate(1)

utime.sleep(1)

i2c = I2C(scl=Pin(5), sda=Pin(4))

oled = ssd1306.SSD1306_I2C(128, 32, i2c)
utime.sleep(1)

graphics = gfx.GFX(128, 32, oled.pixel)
graphics1 = gfx.GFX(128, 64, display.pixel)
graphics2 = gfx.GFX(128, 64, display2.pixel)

utime.sleep(1)

def do_connect():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        wlan.connect(ssid, password)
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

display.fill(0)
display2.fill(0)
display.show()
display2.show()

names = ['Mercury', 'Venus', 'Mars', 'Jupiter', 'Saturn', 'Uranus', 'Neptune']

long_i = [0, 0, 0, 0, 0, 0, 0]
years_i = [0, 0, 0, 0, 0, 0, 0]
longp_i = [0, 0, 0, 0, 0, 0, 0]
period_i = [0, 0, 0, 0, 0, 0, 0]
dist_i = [0, 0, 0, 0, 0, 0, 0]


oled.fill(0)
oled.text('begin loop',0,0,1)
oled.show()
utime.sleep(2)

while True:
    # earth heliocentric longitude
    url = "http://api.wolframalpha.com/v1/result?i=earth%20heliocentric%20longitude%3F&appid=dan_appid"
    r = requests.get(url)
    print(r.text)
    elong = [x.strip() for x in r.text.split(',')]
    elong = [x.strip() for x in elong[0].split()]
    elong = elong[0]
    r.close()
    del r
    print(elong)
    # save planet data to list
    
    for index, name in enumerate(names):
        #oled stuff
        oled.fill(0)
        oled.text("getting:", 0, 0)
        oled.text(name, 0, 10)
        oled.show()
        utime.sleep(2)

        # heliocentric longitude
        url = "http://api.wolframalpha.com/v1/result?i={0}%20heliocentric%20longitude%3F&appid=dan_appid".format(name)
        r = requests.get(url)
        print(r.text)
        long = [x.strip() for x in r.text.split(',')]
        long = [x.strip() for x in long[0].split()]
        long = long[0]
        r.close()
        del r
        print(long)
        # save planet data to list
        long_i[index] = long            
        
        # perihelion data
        url = "http://api.wolframalpha.com/v1/result?i=years%20since%20{0}%20last%20perihelion%3F&appid=dan_appid".format(name)
        r = requests.get(url)
        print(r.text)
        years = [x.strip() for x in r.text.split()]
        years = years[0]
        print(years)
        r.close()
        del r
        gc.collect()
        # save planet data to list
        years_i[index] = years       
        
        # heliocentric longitude @ next perihelion
        url = "http://api.wolframalpha.com/v1/result?i={0}%20heliocentric%20longitude%20at%20next%20perihelion%3F&appid=dan_appid".format(name)
        r = requests.get(url)
        print(r.text)
        longp = [x.strip() for x in r.text.split(',')]
        longp = [x.strip() for x in longp[0].split()]
        longp = longp[0]
        r.close()
        del r
        print(longp)
        # save planet data to list
        longp_i[index] = longp
        
        # orbital period data from wolframalpha API
        url = "http://api.wolframalpha.com/v1/result?i={0}%20orbital%20period%20in%20julian%20years%3F&appid=dan_appid".format(name)
        r = requests.get(url)
        print(r.text)
        period = [x.strip() for x in r.text.split()]
        period = period[0]
        print(period)
        r.close()
        del r
        gc.collect()
        # save planet data to list
        period_i[index] = period       

        
        # distance from earth
        url = "http://api.wolframalpha.com/v1/result?i={0}%20distance%20from%20earth%3F&appid=dan_appid".format(name)
        r = requests.get(url)
        print(r.text)
        dist = [x.strip() for x in r.text.split(',')]
        dist = [x.strip() for x in dist[0].split()]
        dist = dist[1]
        r.close()
        del r
        print(dist)
        # save planet data to list
        dist_i[index] = dist
        
        #oled stuff
        oled.fill(0)
        oled.text(name, 0, 0)
        oled.text("acquired!", 0, 10)
        oled.show()
        utime.sleep(2)


    for index, name in enumerate(names):
        oled.fill(0)
        display.fill(0)
        display2.fill(0)
        oled.show()
        display.show()
        display2.show()
        
        #oled stuff
        pxc = [4, 13, 30, 48, 79, 101, 116]
        pr = [1, 2, 1, 14, 12, 5, 5]
        
        #show planet index graphic
        graphics.circle(pxc[0], 16, pr[0], 1)
        graphics.circle(pxc[1], 16, pr[1], 1)
        graphics.fill_circle(22, 16, 2, 1)
        graphics.circle(pxc[2], 16, pr[2], 1)
        graphics.circle(pxc[3], 16, pr[3], 1)
        graphics.circle(pxc[4], 16, pr[4], 1)
        graphics.circle(pxc[5], 16, pr[5], 1)
        graphics.circle(pxc[6], 16, pr[6], 1)
        oled.line(pxc[index]-pr[index], 31, pxc[index]+pr[index], 31, 1)
        oled.show()
        
        # display stuff
        #calculate progress towards perihelion
        years = float(years_i[index])
        period = float(period_i[index])
        long_i[index] = float(long_i[index])
        
        # orbit progress circle dims
        xc = 62
        yc = 31
        rad = 28
        
        #draw orbit progress circle outline
        graphics1.circle(xc, yc, rad, 1)
        
        #calculate orbit progress in radians
        p_rad = math.radians(long_i[index])
        print(p_rad)
        
        #calculate dimensions of rectangle blocks
        xblock = rad * math.cos(p_rad)
        xblock = round(xblock,0)
        yblock = rad * math.sin(p_rad)
        yblock = round(yblock,0)
        xblock = int(math.fabs(xblock))
        yblock = int(math.fabs(yblock))
        print(xblock, yblock)
        
        #draw rectangle blocks and planet marker
        # top-right
        if p_rad <= math.pi/2:
            #fill bottom half of circle
            display.fill_rect(xc - rad, yc + rad, 2 * rad + 1, rad + 1, 0)
            #fill top left of circle
            display.fill_rect(xc - rad, yc + rad, rad + 1, rad + 1, 0)
            #partial fill top right of circle
            display.fill_rect(xc, yc + rad, xblock + 1, rad + 1, 0)
            #show planet marker
            graphics1.fill_circle(xc + xblock, yc + yblock, 2, 1)
        
        # top-left
        elif p_rad > math.pi/2 and p_rad < math.pi:
           #fill bottom half of circle
            display.fill_rect(xc - rad, yc + rad, 2 * rad + 1, rad + 1, 0)
            #partial fill top left of circle
            display.fill_rect(xc - rad, yc + rad, xblock + 1, rad + 1, 0)
            #show planet marker
            graphics1.fill_circle(xc - xblock, yc + yblock, 2, 1)
         
        # bottom left   
        elif p_rad >= math.pi and p_rad <= 3 * math.pi/2:
           #fill bottom right of circle
            display.fill_rect(xc, yc, rad + 1, rad + 1, 0)
            #partial fill bottom left of circle
            display.fill_rect(xc - rad, yc, xblock + 1, rad + 1, 0)      
            #show planet marker
            graphics1.fill_circle(xc - xblock, yc - yblock, 2, 1)    
        
        # topleft
        else:
            #partial fill bottom right of circle
            display.fill_rect(xc, yc, rad - xblock + 1, rad + 1, 0)
            #show planet marker
            graphics2.fill_circle(xc + xblock, yc - yblock, 2, 1)     
            
        ##make inner demo circle
        #graphics.circle(xc, yc, rad-3, 1)
        #make sun
        graphics1.fill_circle(xc - 4, yc, 4, 1)
        
        #show perihelion and aphelion locations

        display2.show()
        utime.sleep(10)
        
        display.fill(0)
        display2.fill(0)
        display.show()
        display2.show()
    
    # collect garbage just in case that is causing the crashes
    gc.collect()