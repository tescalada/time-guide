import gc

import umatrix as matrix
import ulinalg as linalg

def skyChart(name):
    # display stuff
    oled.text(name, 0, 0)
    oled.text("Visible:", 0,10)
    oled.text(visible_i[names.index(name)], 80,10)
    oled.show()

    # sky chart
    xc = 94
    yc = 31
    rad = 29
    graphics.circle(xc, yc, rad, 1)

    # show planet rise azimuth
    x = int(round(rad * math.cos(math.radians(azr_i[names.index(name)] - 90)),0))
    y = int(round(rad * math.sin(math.radians(azr_i[names.index(name)] - 90)),0))
    xr = xc + x
    yr = yc + y
    graphics.fill_circle(xr, yr, 2, 1)

    # show planet set azimuth
    x = int(round(rad * math.cos(math.radians(azs_i[names.index(name)] - 90)),0))
    y = int(round(rad * math.sin(math.radians(azs_i[names.index(name)] - 90)),0))
    xs = xc + x
    ys = yc + y
    graphics.fill_circle(xs, ys, 2, 1)

    # show location at maximum altitude
    rd = int(round(rad * math.cos(math.radians(alm_i[names.index(name)])),0))
    x = int(round(rd * math.cos(math.radians(azm_i[names.index(name)] - 90)),0))
    y = int(round(rd * math.sin(math.radians(azm_i[names.index(name)] - 90)),0))
    xm = xc + x
    ym = yc + y
    graphics.fill_circle(xm, ym, 2, 1)

    # show current location if visible
    if visible_i[index] == 'Yes':
        rd = int(round(rad * math.cos(math.radians(alc_i[names.index(name)])),0))
        x = int(round(rd * math.cos(math.radians(azc_i[names.index(name)] - 90)),0))
        y = int(round(rd * math.sin(math.radians(azc_i[names.index(name)] - 90)),0))
        xcu = xc + x
        ycu = yc + y
        graphics.circle(xcu, ycu, 2, 1)

    # find path of transit
    A = matrix.matrix([[xr ** 2, xr, 1], [xm ** 2, xm, 1], [xs ** 2, xs, 1]])
    B = matrix.matrix([[yr], [ym], [ys]])
    d_i = linalg.det_inv(A)
    invA = d_i[1]
    X = linalg.dot(invA, B)

    for i in range(xr - xs):
        x = xs + i
        oled.pixel(x, yc - int((X[0] * x ** 2)) + int((X[1] * x)) + int(X[2]), 1)

    oled.show()

    # collect garbage just in case that is causing the crashes
    gc.collect()