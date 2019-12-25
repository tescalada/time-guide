import ssd1306
import sh1106
import gfx
import utime
from shapes3d import sphere, cube

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

oled.fill(0)
oled.text('oled init',0,0,1)
oled.show()


rad = 30
xc = 63
yc = 31
f = yc * 6
xr = 30
yr = 0
zr = 0

sphere(rad, xc, yc, f, xr, yr, zr)
display1.show()
utime.sleep(5)


#rad = 30
#xc = 63
#yc = 31
#f = yc * 8
#xr = 30
#yr = 0
#zr = 0
#
#sphere(rad, xc, yc, f, xr, yr, zr)










