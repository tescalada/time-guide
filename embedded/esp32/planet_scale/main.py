import gc

import ssd1306
import gfx
import math
import utime

#from rotary_irq_esp import RotaryIRQ
from machine import I2C, Pin

oled_reset_pin = Pin(16, Pin.OUT)
oled_reset_pin.value(1)

i2c = I2C(scl=Pin(15), sda=Pin(4))

oled = ssd1306.SSD1306_I2C(128, 64, i2c)
utime.sleep(1)

graphics = gfx.GFX(128, 64, oled.pixel)

oled.fill(0)
oled.text('oled init',0,0,1)
oled.show()
utime.sleep(2)

sdist_i = [0.417, 0.723, 1.64, 5.3, 10.1, 19.8, 29.9]

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

oled.fill(0)
oled.show()

while True:

    for index, name in enumerate(names):
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

        oled.text(name, 16, 0, 1)
        oled.line(pxc[index]-pr[index], 41, pxc[index]+pr[index], 41, 1)
        oled.show()
        utime.sleep(4)


    # collect garbage just in case that is causing the crashes
    gc.collect()