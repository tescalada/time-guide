import gc

import network
import ssd1306
import utime

from machine import I2C, Pin
from credentials import WIFI_SSID, WIFI_PASSWORD

oled_reset_pin = Pin(16, Pin.OUT)
oled_reset_pin.value(1)

i2c = I2C(scl=Pin(15), sda=Pin(4))

oled = ssd1306.SSD1306_I2C(128, 64, i2c)
utime.sleep(1)

oled.fill(0)
oled.text('oled init',0,0,1)
oled.show()
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