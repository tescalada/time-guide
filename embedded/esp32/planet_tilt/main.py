import gc

import ssd1306
import sh1106
import gfx
import utime
import math
import urequests as requests
from credentials import WOLFRAM_API_KEY
from shapes3d import sphere


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

oled.fill(0)
display1.fill(0)
display2.fill(0)


oled.show()
display1.show()
display2.show()

utime.sleep(1)

## create log scale of sizes of planets
#arb = 0.26
#pre = [1, 2.48, 2.61, 1.39, 28.66, 23.9, 10.4, 10.1]
#pre.insert(0, arb)
#scale = 15
#pre = [scale * math.log(x/pre[0],10) for x in pre]
#pre.pop(0)
#pre = [int(math.ceil(x)) for x in pre]
#
#period = [0.2408467, 0.615197, 1, 1.8808476, 11.862615, 29.447498, 84.016846, 164.79132]
#tilt = [0, 2, 34, 25, 3, 27, 98, 28]
#siderial = [58, 243, 1, 1, 0.4, 0.4, 0.7, 0.7]
#
#url = "http://api.wolframalpha.com/v1/result?i=today%3F&appid={0}".format(WOLFRAM_API_KEY)
#r = requests.get(url)
#print(r.text)
#today = [x.strip() for x in r.text.split(',')]
#today = [x.strip() for x in today[1].split()]
#today = today[0]

n = 0

while n >= 0:
    rad = 30
    xc = int(65 + 50 * math.sin(n))
    yc = int(33 + 20 * math.sin(n))
    f = int(121 + 120 * math.cos(n))
    xr = 0
    yr = int(n * 25)
    zr = 23
    sphere(rad, xc, yc, f, xr, yr, zr)

    n += 0.25


    # collect garbage just in case that is causing the crashes
    gc.collect()