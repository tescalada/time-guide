import machine, neopixel
import utime as time

n = 9
p = 13
np = neopixel.NeoPixel(machine.Pin(p), n, bpp=4)

rise = []
sett = []

# open csv files with rise/set data

n_Rows = 0
with open('rise.csv','r') as file:
	for line in file:
		line=line.rstrip('\n')
		line=line.rstrip('\r')
		rise.append(line.split(','))
		n_Rows += 1

n_Rows = 0 #used to find out the number of rows in the file
with open('sett.csv','r') as file:
	for line in file:
		line=line.rstrip('\n')
		line=line.rstrip('\r')
		sett.append(line.split(','))
		n_Rows += 1

## convert rise/set hours into notelists for mixer
# note duration
val = 64

# note list for each body
LED = [(255, 255, 0, 128),
       (50, 50, 50, 64),
       (212, 102, 102, 0),
       (241, 232, 184, 0),
       (46, 118, 255, 0),
       (255, 0, 0, 0),
       (250, 149, 0, 0),
       (255, 218, 198, 0),
       (54, 65, 86, 0),
       (70, 35, 206, 0)]


for i in range(len(rise)):
    for j in range(24):
        #sun
        if int(rise[i][0]) + (i * 24) - 1 == i * 24 + j or int(sett[i][0]) + (i * 24) - 1 == i * 24 + j:
            np[0] = LED[0]
        else:
            np[0] = (0, 0, 0, 0)
        #moon
        if int(rise[i][1]) + (i * 24) - 1 == i * 24 + j or int(sett[i][1]) + (i * 24) - 1 == i * 24 + j:
            np[1] = LED[1]
        else:
            np[1] = (0, 0, 0, 0)
        #me
        if int(rise[i][2]) + (i * 24) - 1 == i * 24 + j or int(sett[i][2]) + (i * 24) - 1 == i * 24 + j:
            np[2] = LED[2]
        else:
            np[2] = (0, 0, 0, 0)
        #ve
        if int(rise[i][3]) + (i * 24) - 1 == i * 24 + j or int(sett[i][3]) + (i * 24) - 1 == i * 24 + j:
            np[3] = LED[3]
        else:
            np[3] = (0, 0, 0, 0)
        #ma
        if int(rise[i][4]) + (i * 24) - 1 == i * 24 + j or int(sett[i][4]) + (i * 24) - 1 == i * 24 + j:
            np[4] = LED[4]
        else:
            np[4] = (0, 0, 0, 0)
        #ju
        if int(rise[i][5]) + (i * 24) - 1 == i * 24 + j or int(sett[i][5]) + (i * 24) - 1 == i * 24 + j:
            np[5] = LED[5]
        else:
            np[5] = (0, 0, 0, 0)
        #sa
        if int(rise[i][6]) + (i * 24) - 1 == i * 24 + j or int(sett[i][6]) + (i * 24) - 1 == i * 24 + j:
            np[6] = LED[6]
        else:
            np[6] = (0, 0, 0, 0)
        #ur
        if int(rise[i][7]) + (i * 24) - 1 == i * 24 + j or int(sett[i][7]) + (i * 24) - 1 == i * 24 + j:
            np[7] = LED[7]
        else:
            np[7] = (0, 0, 0, 0)
         #ne
        if int(rise[i][8]) + (i * 24) - 1 == i * 24 + j or int(sett[i][8]) + (i * 24) - 1 == i * 24 + j:
            np[8] = LED[8]
        else:
            np[8] = (0, 0, 0, 0)

        np.write()
        time.sleep(0.5)




# def demo(np):

#     # # cycle
#     # for i in range(4 * n):
#     #     for j in range(n):
#     #         np[j] = (0, 0, 0, 0)
#     #     np[i % n] = (255, 255, 255, 255)
#     #     np.write()
#     #     time.sleep_ms(100)

#     # bounce
#     for i in range(4 * n):
#         for j in range(n):
#             np[j] = (75, 156, 211, 0)
#         if (i // n) % 2 == 0:
#             np[i % n] = (0, 0, 0, 0)
#         else:
#             np[n - 1 - (i % n)] = (0, 0, 0, 0)
#         np.write()
#         time.sleep_ms(500)

#     # # fade in/out
#     # for i in range(0, 4 * 256, 8):
#     #     for j in range(n):
#     #         if (i // 256) % 2 == 0:
#     #             val = i & 0xff
#     #         else:
#     #             val = 255 - (i & 0xff)
#     #         np[j] = (val, 0, 0, 0)
#     #     np.write()

#     # clear
#     for i in range(n):
#         np[i] = (0, 0, 0, 0)
#     np.write()

# demo(np)



