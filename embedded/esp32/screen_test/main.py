import gc

import network
import ssd1306
import sh1106
import utime
import gfx

from machine import I2C, Pin, SPI
from credentials import WIFI_SSID, WIFI_PASSWORD

oled_reset_pin = Pin(16, Pin.OUT)
oled_reset_pin.value(1)

spi = SPI(1, baudrate=800000)

display = sh1106.SH1106_SPI(128, 64, spi, dc=Pin(0), res=oled_reset_pin, cs=Pin(2))
utime.sleep(1)

display2 = sh1106.SH1106_SPI(128, 64, spi, dc=Pin(17), res=oled_reset_pin, cs=Pin(5))
utime.sleep(1)

display.sleep(False)
display.rotate(1)
utime.sleep(1)

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
graphics.circle(63, 32, 10, 1)

display.fill(0)
display.text('display init',0,0,1)
graphics1.circle(63, 32, 10, 1)

display2.fill(0)
display2.text('display2 init',0,0,1)
graphics2.circle(63, 32, 10, 1)

oled.show()
display.show()
display2.show()

utime.sleep(2)


def do_connect():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        wlan.connect(WIFI_SSID, WIFI_PASSWORD)
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