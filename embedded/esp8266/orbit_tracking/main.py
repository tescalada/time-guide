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

display.fill(1)
display2.fill(1)
display.show()
display2.show()
    
# list values as of 6/17/2019
long_i = [200.0, 48.0, 126.0, 260.0, 286.0, 33.0, 346.0]
years_i = ['August 20, 2019', 'August 8, 2019', 'August 3, 2020', 'January 24, 2023', 'December 24, 2032', 'February 10, 2051', 'July 16, 2047']
longp_i = [76.0, 131.0, 336.0, 14.0, 93.0, 173.0, 49.0]
period_i = [0.2408467, 0.61519726, 1.8808476, 11.862615, 29.447498, 84.016846, 164.79132]
dist_i = [0.928, 1.65, 2.51, 4.29, 9.1, 20.5, 29.8]
sdist_i = [0.417, 0.723, 1.64, 5.3, 10.1, 19.8, 29.9]

names = ['Mercury', 'Venus', 'Mars', 'Jupiter', 'Saturn', 'Uranus', 'Neptune']

oled.fill(0)
oled.text('begin loop',0,0,1)
oled.show()
utime.sleep(1)

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
    elong = float(elong)
    elong = math.radians(elong)

   #oled stuff
   # make log10 orbit distances
        
    url = "http://api.wolframalpha.com/v1/result?i=earth%20distance%20from%20sun%3F&appid=dan_appid"
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
        long_i[index] = float(long)         
     
        # perihelion data
        url = "http://api.wolframalpha.com/v1/result?i={0}%20next%20periapsis%3F&appid=dan_appid".format(name)
        r = requests.get(url)
        print(r.text)
        years = r.text
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
        longp_i[index] = float(longp)
        
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
        period_i[index] = float(period)       

         # distance from sun
        url = "http://api.wolframalpha.com/v1/result?i={0}%20distance%20from%20sun%3F&appid=dan_appid".format(name)
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
        dist_i[index] = float(dist)
        
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
        display.fill(0)
        display2.fill(0)
        oled.show()
        display.show()
        display2.show()
        
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
        
        # display stuff
        #calculate progress towards perihelion
        # orbit progress circle dims
        xc = 63
        yc = 31
        rad = int(pxc[index]/4)
        
        #draw orbit progress circle outline
        graphics1.circle(xc, yc, rad, 1)
        
        #calculate orbit progress in radians
        p_rad = math.radians(long_i[index])
        print(p_rad)
        
        #calculate x,y position of planet in heliocentric coordinates relative to xc,yc
        xp = int(round(rad * math.cos(p_rad),0))
        yp = int(round(rad * math.sin(p_rad),0))

        #draw rectangle blocks and planet marker
        xblock = int(math.fabs(xp))

        # top-right
        if p_rad <= math.pi/2:
            #fill bottom half of circle
            display.fill_rect(xc - rad, yc, 2 * rad + 1, rad + 1, 0)
            #fill top left of circle
            display.fill_rect(xc - rad, yc - rad, rad + 1, rad + 1, 0)
            #partial fill top right of circle
            display.fill_rect(xc, yc - rad, xblock + 1, rad + 1, 0) 

        # top-left
        elif p_rad >= math.pi/2 and p_rad <= math.pi:
           #fill bottom half of circle
            display.fill_rect(xc - rad, yc, 2 * rad + 1, rad + 1, 0)
            #partial fill top left of circle
            display.fill_rect(xc - rad, yc - rad, rad - xblock, rad + 1, 0)

        # bottom left   
        elif p_rad >= math.pi and p_rad <= 3 * math.pi/2:
           #fill bottom right of circle           
            display.fill_rect(xc, yc, rad + 1, rad + 1, 0)
            #partial fill bottom left of circle
            display.fill_rect(xc - xblock, yc, xblock + 1, rad + 1, 0)
            
        # bottom-right
        else:
            #partial fill bottom right of circle
            display.fill_rect(xc + xblock, yc, rad - xblock + 1, rad + 1, 0)

        # plot planet marker
        graphics1.circle(xc + xp, yc - yp, pr[index], 1)
        graphics1.fill_circle(xc + xp, yc - yp, 1, 1)

        # plot earth
        xe = int(round((sdist_i[2]/4) * math.cos(elong),0))
        ye = int(round((sdist_i[2]/4) * math.sin(elong),0))
        graphics1.circle(xc + xe, yc - ye, 1, 1)

#        # plot earth - planet distance
#        display.line(xc + xp, yc + yp, xc + xe, yc + ye, 1)

        # make sun
        graphics1.fill_circle(xc, yc, 2, 1)
     
        # show perihelion location
        longp = longp_i[index]
        longp = math.radians(longp)
        xpp = int((rad) * math.cos(longp))
        ypp = int((rad) * math.sin(longp))
        display.line(xc, yc, xc + xpp, yc + ypp, 1)        
        
        
        # display2 stuff
        # show data
        display2.text('heliocentric longitude: ',0,0)
        display2.text(long_i[index],100,0)

        display2.text('dist to earth (AU): ',0,10)
        display2.text(round(dist_i[index],2),100,10)

        display2.text('next periapsis:',0,20)
        display2.text(years_i[index],100,20)

        display2.text('orbital period:',0,30)
        display2.text(round(period_i[index],2),100,30)

        display.show()
        display2.show()
        utime.sleep(10)
        
        oled.fill(0)
        display.fill(0)
        display2.fill(0)
        oled.show()
        display.show()
        display2.show()
        
    
    # collect garbage just in case that is causing the crashes
    gc.collect()