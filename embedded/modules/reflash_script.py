# for esp8266 board
wget http://micropython.org/resources/firmware/esp8266-20190529-v1.11.bin
esptool.py --port /dev/tty.usbserial-0001 erase_flash
esptool.py --port /dev/tty.usbserial-0001 --baud 460800 write_flash --flash_size=detect 0 esp8266-20190529-v1.11.bin

# for esp32 board
wget https://micropython.org/resources/firmware/esp32-idf3-20200902-v1.13.bin

esptool.py --chip esp32 --port /dev/tty.usbserial-0001 erase_flash
esptool.py --chip esp32 --port /dev/tty.usbserial-0001 --baud 460800 write_flash -z 0x1000 esp32-20190529-v1.11.bin
esptool.py --chip esp32 --port /dev/tty.usbserial-0001 --baud 460800 write_flash -z 0x1000 esp32-idf3-20200902-v1.13.bin


# put modules
cd Documents/GitHub/time-guide/embedded/modules
ampy --port /dev/tty.usbserial-0001 --baud 115200 put ssd1306.py
ampy --port /dev/tty.usbserial-0001 --baud 115200 put sh1106.py
ampy --port /dev/tty.usbserial-0001 --baud 115200 put gfx.py
ampy --port /dev/tty.usbserial-0001 --baud 115200 put PlanetFn.py
ampy --port /dev/tty.usbserial-0001 --baud 115200 put shapes3d.py


cd micropython-rotary-master
ampy --port /dev/tty.usbserial-0001 --baud 115200 put rotary.py
ampy --port /dev/tty.usbserial-0001 --baud 115200 put rotary_irq_esp.py

cd ..
cd ..
cd esp32/planet_scale
ampy --port /dev/tty.usbserial-0001 --baud 115200 put main.py
ampy --port /dev/tty.usbserial-0001 --baud 115200 put credentials.py


screen /dev/tty.usbserial-0001 115200
# in screen, hit CTRL-A, k, y to quit and return to terminal



# check ports
ls /dev/tty.*

# run scron on board
micropython -m upip install -p modules micropython-scron