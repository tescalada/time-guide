import gc

import ssd1306
import sh1106
import gfx
import utime
import math

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


def cube(rad, xc, yc, f, xr, yr, zr):
    ## transforms
    # x-transform, y-transform, z-transform
    rot = [math.radians(xr), math.radians(yr), math.radians(zr)] #degrees rotation
#    scale = [0, 0, 0] #scale multiplier - not yet used
#    translate = [0, 0, 0] #translate addition - not yet used

    xrot = [
    [1, 0, 0],
    [0, math.cos(rot[0]), -math.sin(rot[0])],
    [0, math.sin(rot[0]), math.cos(rot[0])],
    ]

    yrot = [
    [math.cos(rot[1]), 0, math.sin(rot[1])],
    [0, 1, 0],
    [-math.sin(rot[1]), 0, math.cos(rot[1])],
    ]

    zrot = [
    [math.cos(rot[2]), -math.sin(rot[2]), 0],
    [math.sin(rot[2]), math.cos(rot[2]), 0],
    [0, 0, 1]
    ]

    xrottr = list(map(list, zip(*xrot)))
    yrottr = list(map(list, zip(*yrot)))
    zrottr = list(map(list, zip(*zrot)))

    #generate cube points
    coords3 = [
    [rad * 0.7071, rad * 0.7071, -rad * 0.7071],
    [rad * 0.7071, rad * 0.7071, rad * 0.7071],
    [-rad * 0.7071, rad * 0.7071, rad * 0.7071],
    [-rad * 0.7071, rad * 0.7071, -rad * 0.7071],
    [rad * 0.7071, -rad * 0.7071, -rad * 0.7071],
    [rad * 0.7071, -rad * 0.7071, rad * 0.7071],
    [-rad * 0.7071, -rad * 0.7071, rad * 0.7071],
    [-rad * 0.7071, -rad * 0.7071, -rad * 0.7071]
    ]

    gc.collect()

    coords3tx = [[0 for col in range(len(coords3[0]))] for row in range(len(coords3))]
    coords3ty = [[0 for col in range(len(coords3[0]))] for row in range(len(coords3))]
    coords3tz = [[0 for col in range(len(coords3[0]))] for row in range(len(coords3))]

    # dot product of two lists:
    for x in range(len(coords3)):
        for y in range(3):
            coords3tx[x][y] = sum(i * j for i, j in zip(xrottr[y], coords3[x]))

    del coords3
    gc.collect()

    for x in range(len(coords3tx)):
        for y in range(3):
            coords3ty[x][y] = sum(i * j for i, j in zip(yrottr[y], coords3tx[x]))

    del coords3tx
    gc.collect()

    for x in range(len(coords3ty)):
        for y in range(3):
            coords3tz[x][y] = sum(i * j for i, j in zip(zrottr[y], coords3ty[x]))

    del coords3ty
    gc.collect()

    # make 2d projection from XYZ world coordinates
    center = [0, 0, 10 * rad + 1]

    X3 = [column[0] + center[0] for column in coords3tz]
    Y3 = [column[1] + center[1] for column in coords3tz]
    Z3 = [column[2] + center[2] for column in coords3tz]

    del coords3tz
    gc.collect()

    X2 = [int(f * x / z + xc) for x, z in zip (X3, Z3)]
    Y2 = [int(-f * y / z + yc) for y, z in zip (Y3, Z3)]

    del X3, Y3, Z3
    gc.collect()

    display1.fill(0)
    for i in range(3):
        # draw top half
        graphics1.line(X2[i], Y2[i], X2[i + 1], Y2[i + 1], 1)
        # draw bottom half
        graphics1.line(X2[i + 4], Y2[i + 4], X2[i + 5], Y2[i + 5], 1)
        # draw middle lines
        graphics1.line(X2[i], Y2[i], X2[i + 4], Y2[i + 4], 1)

    #draw last connecting lines
    graphics1.line(X2[3], Y2[3], X2[0], Y2[0], 1)
    graphics1.line(X2[7], Y2[7], X2[4], Y2[4], 1)
    graphics1.line(X2[7], Y2[7], X2[3], Y2[3], 1)
    display1.show()

    gc.collect()


## Sphere
def sphere(rad, xc, yc, f, xr, yr, zr):

    ## transforms
    # x-transform, y-transform, z-transform
    rot = [math.radians(xr), math.radians(yr), math.radians(zr)] #degrees rotation
#    scale = [0, 0, 0] #scale multiplier - not yet used
#    translate = [0, 0, 0] #translate addition - not yet used

    xrot = [
    [1, 0, 0],
    [0, math.cos(rot[0]), -math.sin(rot[0])],
    [0, math.sin(rot[0]), math.cos(rot[0])],
    ]

    yrot = [
    [math.cos(rot[1]), 0, math.sin(rot[1])],
    [0, 1, 0],
    [-math.sin(rot[1]), 0, math.cos(rot[1])],
    ]

    zrot = [
    [math.cos(rot[2]), -math.sin(rot[2]), 0],
    [math.sin(rot[2]), math.cos(rot[2]), 0],
    [0, 0, 1]
    ]

    xrottr = list(map(list, zip(*xrot)))
    yrottr = list(map(list, zip(*yrot)))
    zrottr = list(map(list, zip(*zrot)))

    #generate sphere points
    coords3 = [[0 for col in range(3)] for row in range(62)]

    theta = [60, 30, 0, -30, -60]

    coords3[0] = [0, rad, 0]
    for i in range(5):
        for j in range(12):
            coords3[(i * 12) + j + 1][0] = rad * math.sin(math.radians(90 - theta[i])) * math.cos(math.radians(30 * j))
            coords3[(i * 12) + j + 1][1] = rad * math.cos(math.radians(90 - theta[i]))
            coords3[(i * 12) + j + 1][2] = rad * math.sin(math.radians(90 - theta[i])) * math.sin(math.radians(30 * j))
    coords3[61] = [0, -rad, 0]

    gc.collect()

    coords3tx = [[0 for col in range(len(coords3[0]))] for row in range(len(coords3))]
    coords3ty = [[0 for col in range(len(coords3[0]))] for row in range(len(coords3))]
    coords3tz = [[0 for col in range(len(coords3[0]))] for row in range(len(coords3))]

    # dot product of two lists:
    for x in range(len(coords3)):
        for y in range(3):
            coords3tx[x][y] = sum(i * j for i, j in zip(xrottr[y], coords3[x]))

    del coords3
    gc.collect()

    for x in range(len(coords3tx)):
        for y in range(3):
            coords3ty[x][y] = sum(i * j for i, j in zip(yrottr[y], coords3tx[x]))

    del coords3tx
    gc.collect()

    for x in range(len(coords3ty)):
        for y in range(3):
            coords3tz[x][y] = sum(i * j for i, j in zip(zrottr[y], coords3ty[x]))

    del coords3ty
    gc.collect()

    # make 2d projection from XYZ world coordinates
    center = [0, 0, 10 * rad + 1]

    X3 = [column[0] + center[0] for column in coords3tz]
    Y3 = [column[1] + center[1] for column in coords3tz]
    Z3 = [column[2] + center[2] for column in coords3tz]

    del coords3tz
    gc.collect()

    X2 = [int(f * x / z + xc) for x, z in zip (X3, Z3)]
    Y2 = [int(-f * y / z + yc) for y, z in zip (Y3, Z3)]

    del X3, Y3, Z3
    gc.collect()

    display1.fill(0)
    for i in range(12):
        #top to 60
        graphics1.line(X2[0], Y2[0], X2[i + 1], Y2[i + 1], 1)
        #60 to 30
        graphics1.line(X2[i + 1], Y2[i + 1], X2[i + 13], Y2[i + 13], 1)
        #30 to 0
        graphics1.line(X2[i + 13], Y2[i + 13], X2[i + 25], Y2[i + 25], 1)
        #0 to -30
        graphics1.line(X2[i + 25], Y2[i + 25], X2[i + 37], Y2[i + 37], 1)
        #-30 to -60
        graphics1.line(X2[i + 37], Y2[i + 37], X2[i + 49], Y2[i + 49], 1)
        #-60 to bottom
        graphics1.line(X2[i + 49], Y2[i + 49], X2[61], Y2[61], 1)

    for i in range(11):
        #60 line
        graphics1.line(X2[i + 1], Y2[i + 1], X2[i + 2], Y2[i + 2], 1)
        #30 line
        graphics1.line(X2[i + 13], Y2[i + 13], X2[i + 14], Y2[i + 14], 1)
        #0 line
        graphics1.line(X2[i + 25], Y2[i + 25], X2[i + 26], Y2[i + 26], 1)
        #-30 line
        graphics1.line(X2[i + 37], Y2[i + 37], X2[i + 38], Y2[i + 38], 1)
        #-60 line
        graphics1.line(X2[i + 49], Y2[i + 49], X2[i + 50], Y2[i + 50], 1)

    #missing lines
    #60 line
    graphics1.line(X2[1], Y2[1], X2[12], Y2[12], 1)
    #30 line
    graphics1.line(X2[13], Y2[13], X2[24], Y2[24], 1)
    #0 line
    graphics1.line(X2[25], Y2[25], X2[36], Y2[36], 1)
    #-30 line
    graphics1.line(X2[37], Y2[37], X2[48], Y2[48], 1)
    #-60 line
    graphics1.line(X2[49], Y2[49], X2[60], Y2[60], 1)

    display1.show()
    gc.collect()