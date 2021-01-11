import machine, neopixel
import time

n = 9
p = 13
np = neopixel.NeoPixel(machine.Pin(p), n, bpp=4)

# np[0] = (0, 0, 0, 64)
# np[1] = (64, 0, 0, 0)
# np[2] = (0, 64, 0, 0)
# np[3] = (0, 0, 64, 0)
# np[4] = (0, 0, 0, 64)
# np[5] = (0, 0, 0, 64)
# np[6] = (0, 0, 0, 64)
# np[7] = (0, 0, 0, 64)
# np[8] = (0, 0, 0, 64)
# time.sleep(0.5)


def demo(np):

    # # cycle
    # for i in range(4 * n):
    #     for j in range(n):
    #         np[j] = (0, 0, 0, 0)
    #     np[i % n] = (255, 255, 255, 255)
    #     np.write()
    #     time.sleep_ms(100)

    # bounce
    for i in range(4 * n):
        for j in range(n):
            np[j] = (75, 156, 211, 0)
        if (i // n) % 2 == 0:
            np[i % n] = (0, 0, 0, 0)
        # else:
        #     np[n - 1 - (i % n)] = (0, 0, 0, 0)
        np.write()
        time.sleep_ms(500)

    # # fade in/out
    # for i in range(0, 4 * 256, 8):
    #     for j in range(n):
    #         if (i // 256) % 2 == 0:
    #             val = i & 0xff
    #         else:
    #             val = 255 - (i & 0xff)
    #         np[j] = (val, 0, 0, 0)
    #     np.write()

    # clear
    for i in range(n):
        np[i] = (0, 0, 0, 0)
    np.write()

demo(np)



