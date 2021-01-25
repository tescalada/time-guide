import machine, neopixel
import utime as time

# define variables
names = ['Sun', 'Moon', 'Mercury', 'Venus', 'Mars', 'Jupiter', 'Saturn', 'Uranus', 'Neptune']

#initialize neopixel
n = 81
p = 13
np = neopixel.NeoPixel(machine.Pin(p), n, bpp=4)

# LED list for each body
LED = [(0, 0, 0, 25),
       (0, 0, 0, 50),
       (0, 0, 0, 75),
       (0, 0, 0, 100),
       (0, 0, 0, 125),
       (0, 0, 0, 150),
       (0, 0, 0, 175),
       (0, 0, 0, 200),
       (0, 0, 0, 225),
       (0, 0, 0, 250)]

for i in range(len(names)):
    planet_num = i

    np[planet_num * 9] = LED[planet_num]
    np[planet_num * 9 + 1] = LED[planet_num]
    np[planet_num * 9 + 2] = LED[planet_num]
    np[planet_num * 9 + 3] = LED[planet_num]
    np[planet_num * 9 + 4] = LED[planet_num]
    np[planet_num * 9 + 5] = LED[planet_num]
    np[planet_num * 9 + 6] = LED[planet_num]
    np[planet_num * 9 + 7] = LED[planet_num]
    np[planet_num * 9 + 8] = LED[planet_num]
    np.write()

    time.sleep(1)

    np[planet_num * 9] = (0, 0, 0, 0)
    np[planet_num * 9 + 1] = (0, 0, 0, 0)
    np[planet_num * 9 + 2] = (0, 0, 0, 0)
    np[planet_num * 9 + 3] = (0, 0, 0, 0)
    np[planet_num * 9 + 4] = (0, 0, 0, 0)
    np[planet_num * 9 + 5] = (0, 0, 0, 0)
    np[planet_num * 9 + 6] = (0, 0, 0, 0)
    np[planet_num * 9 + 7] = (0, 0, 0, 0)
    np[planet_num * 9 + 8] = (0, 0, 0, 0)
    np.write()

