import ssd1306
import sh1106
import gfx
import utime
import urandom as random

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

# define 6 points of octahedron

rad = 30
center = [0, 0, rad + 1]

# transforms
lat_tilt = 0
long_tilt = 0
x_trans = 0
y_trans = 0
z_trans = 0

transform = [
[cos(rot_xy)]
        ]


coords3 = [
[center[0], center[1] + rad, center[2]],
[center[0], center[1], center[2] - rad],
[center[0] + rad, center[1], center[2]],
[center[0], center[1], center[2] + rad],
[center[0] - rad, center[1], center[2]],
[center[0], center[1] - rad, center[2]]
]


# define edges


# focal length
xc = 63
yc = 31
f = yc

X3 = [column[0] for column in coords3]
Y3 = [column[1] for column in coords3]
Z3 = [column[2] for column in coords3]

X2 = [int(f * x / z + xc) for x, z in zip (X3, Z3)]
Y2 = [int(-f * y / z + yc) for y, z in zip (Y3, Z3)]

print(X2)
print(Y2)

for i in range(len(X2) - 2):
    # draw top half
    graphics1.line(X2[0], Y2[0], X2[i + 1], Y2[i + 1], 1)
    # draw bottom half
    graphics1.line(X2[5], Y2[5], X2[i + 1], Y2[i + 1], 1)

for i in range(len(X2) -3):
    graphics1.line(X2[i + 1], Y2[i + 1], X2[i + 2], Y2[i + 2], 1)

graphics1.line(X2[1], Y2[1], X2[4], Y2[4], 1)

display1.show()
































