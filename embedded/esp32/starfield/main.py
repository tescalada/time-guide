import ssd1306
import sh1106
import gfx
import utime
import urandom as random

from machine import I2C, Pin, SPI

oled_reset_pin = Pin(16, Pin.OUT)

hspi = SPI(1, 10000000, sck=Pin(18), mosi=Pin(23), miso=Pin(19))

display = sh1106.SH1106_SPI(128, 64, hspi, dc=Pin(26), res=oled_reset_pin, cs=Pin(5))
display2 = sh1106.SH1106_SPI(128, 64, hspi, dc=Pin(33), res=oled_reset_pin, cs=Pin(2))

utime.sleep(1)

display.sleep(False)
display.rotate(1)
display2.sleep(False)
display2.rotate(1)
utime.sleep(1)

i2c = I2C(scl=Pin(15), sda=Pin(4))

oled = ssd1306.SSD1306_I2C(128, 64, i2c)
utime.sleep(1)

graphics = gfx.GFX(128, 64, oled.pixel)
graphics1 = gfx.GFX(128, 64, display.pixel)
graphics2 = gfx.GFX(128, 64, display2.pixel)

oled.fill(0)
oled.text('oled init',0,0,1)
oled.show()
utime.sleep(1)

def initStar(i):
    if random.getrandbits(1) == 0:
        sign = 1
    else:
        sign = -1

    star_x[i] = int(100 * sign * random.getrandbits(9)/512)

    if random.getrandbits(1) == 0:
        sign = 1
    else:
        sign = -1

    star_y[i] = int(100 * sign * random.getrandbits(9)/512)

    star_z[i] = 100 + int(400 * random.getrandbits(9)/512)

def showStarfield():
    for i in range(stars):

        star_z[i] = star_z[i] - 10

        if star_z[i] < 1:
            initStar(i)

        x = int(star_x[i] / star_z[i] * 100 + xc)
        y = int(star_y[i] / star_z[i] * 100 + yc)

        if x < 0 or y < 0 or x > 127 or y > 63:
            initStar(i)

        oled.pixel(x, y, 1)
        display.pixel(x, y, 1)
        display2.pixel(x, y, 1)

    oled.show()
    display.show()
    display2.show()

stars = 500
star_x = list(range(stars))
star_y = list(range(stars))
star_z = list(range(stars))

xc = 63;
yc = 31;

for i in range(stars):
    initStar(i)

while True:
    oled.fill(0)
    display.fill(0)
    display2.fill(0)
    showStarfield()