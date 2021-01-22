from datetime import datetime
import csv

from tones import SINE_WAVE
from tones.mixer import Mixer

names = ['Sun', 'Moon', 'Mercury', 'Venus', 'Mars', 'Jupiter', 'Saturn', 'Uranus', 'Neptune']

## get csv rise/set data into python variables
# open csv files with rise/set data
with open('planet_rise.csv', newline='') as f:
    reader = csv.reader(f)
    rise = list(reader)

with open('planet_set.csv', newline='') as f:
    reader = csv.reader(f)
    sett = list(reader)

# delete column headers in first row
del rise[0]
del sett[0]

#parse sunrise strings, which start with "at "
for index in range(len(rise)):
    #parse string by spaces
    rise[index][0] = [x.strip() for x in rise[index][0].split(' ')]
    sett[index][0] = [x.strip() for x in sett[index][0].split(' ')]
    #delete "at " from list
    del rise[index][0][0]
    del sett[index][0][0]

#parse all other strings
for i in range(len(rise)):
    for j in range(len(names) - 1):
        #parse string by spaces
        rise[i][j+1] = [x.strip() for x in rise[i][j+1].split(' ')]
        sett[i][j+1] = [x.strip() for x in sett[i][j+1].split(' ')]

#parse whole list, convert to 24h time and keep only the hour
for i in range(len(rise)):
    for j in range(len(names)):
        if rise[i][j][1] == 'A.M.':
            rise[i][j] = rise[i][j][0] + ' AM'
        else:
            rise[i][j] = rise[i][j][0] + ' PM'

        if sett[i][j][1] == 'A.M.':
            sett[i][j] = sett[i][j][0] + ' AM'
        else:
            sett[i][j] = sett[i][j][0] + ' PM'

        rise[i][j] = datetime.strptime(rise[i][j], "%I:%M %p")
        sett[i][j] = datetime.strptime(sett[i][j], "%I:%M %p")

        rise[i][j] = int(datetime.strftime(rise[i][j], "%H"))
        sett[i][j] = int(datetime.strftime(sett[i][j], "%H"))

# write csv files with rise/set hours
file = open('rise.csv', 'w+', newline ='')
with file:
    write = csv.writer(file)
    write.writerows(rise)

file = open('sett.csv', 'w+', newline ='')
with file:
    write = csv.writer(file)
    write.writerows(sett)


## convert rise/set hours into notelists for mixer
# note duration
dur = 0.5

# note list for each body
bnotes = [('d', 4, dur, 0, 0, 0.1, 0.3),
         ('g', 4, dur, 0, 0, 0.1, 0.3),
         ('c', 5, dur, 0, 0, 0.1, 0.3),
         ('e', 5, dur, 0, 0, 0.1, 0.3),
         ('g', 5, dur, 0, 0, 0.1, 0.3),
         ('f#', 4, dur, 0, 0, 0.1, 0.3),
         ('a', 4, dur, 0, 0, 0.1, 0.3),
         ('a', 5, dur, 0, 0, 0.1, 0.3),
         ('d', 5, dur, 0, 0, 0.1, 0.3)
         ]

silence = (0, 0)

#create notelist for each planet
notelist_sun = [bnotes[0] + silence for i in range(24 * len(rise))]
notelist_moon = [bnotes[1] + silence for i in range(24 * len(rise))]
notelist_me = [bnotes[2] + silence for i in range(24 * len(rise))]
notelist_ve = [bnotes[3] + silence for i in range(24 * len(rise))]
notelist_ma = [bnotes[4] + silence for i in range(24 * len(rise))]
notelist_ju = [bnotes[5] + silence for i in range(24 * len(rise))]
notelist_sa = [bnotes[6] + silence for i in range(24 * len(rise))]
notelist_ur = [bnotes[7] + silence for i in range(24 * len(rise))]
notelist_ne = [bnotes[8] + silence for i in range(24 * len(rise))]


for i in range(len(rise)):
    for j in range(24):
        #sun
        if rise[i][0] + (i * 24) - 1 == i * 24 + j or sett[i][0] + (i * 24) - 1 == i * 24 + j:
            notelist_sun[i * 24 + j] = bnotes[0]
        else:
            notelist_sun[i * 24 + j] = notelist_sun[i * 24 + j]
        #mooon
        if rise[i][1] + (i * 24) - 1 == i * 24 + j or sett[i][1] + (i * 24) - 1 == i * 24 + j:
            notelist_moon[i * 24 + j] = bnotes[1]
        else:
            notelist_moon[i * 24 + j] = notelist_moon[i * 24 + j]
        #mercury
        if rise[i][2] + (i * 24) - 1 == i * 24 + j or sett[i][2] + (i * 24) - 1 == i * 24 + j:
            notelist_me[i * 24 + j] = bnotes[2]
        else:
            notelist_me[i * 24 + j] = notelist_me[i * 24 + j]
        #venus
        if rise[i][3] + (i * 24) - 1 == i * 24 + j or sett[i][3] + (i * 24) - 1 == i * 24 + j:
            notelist_ve[i * 24 + j] = bnotes[3]
        else:
            notelist_ve[i * 24 + j] = notelist_ve[i * 24 + j]
        #mars
        if rise[i][4] + (i * 24) - 1 == i * 24 + j or sett[i][4] + (i * 24) - 1 == i * 24 + j:
            notelist_ma[i * 24 + j] = bnotes[4]
        else:
            notelist_ma[i * 24 + j] = notelist_ma[i * 24 + j]
        #jupiter
        if rise[i][5] + (i * 24) - 1 == i * 24 + j or sett[i][5] + (i * 24) - 1 == i * 24 + j:
            notelist_ju[i * 24 + j] = bnotes[5]
        else:
            notelist_ju[i * 24 + j] = notelist_ju[i * 24 + j]
        #saturn
        if rise[i][6] + (i * 24) - 1 == i * 24 + j or sett[i][6] + (i * 24) - 1 == i * 24 + j:
            notelist_sa[i * 24 + j] = bnotes[6]
        else:
            notelist_sa[i * 24 + j] = notelist_sa[i * 24 + j]
        #uranus
        if rise[i][7] + (i * 24) - 1 == i * 24 + j or sett[i][7] + (i * 24) - 1 == i * 24 + j:
            notelist_ur[i * 24 + j] = bnotes[7]
        else:
            notelist_ur[i * 24 + j] = notelist_ur[i * 24 + j]
        #neptune
        if rise[i][8] + (i * 24) - 1 == i * 24 + j or sett[i][8] + (i * 24) - 1 == i * 24 + j:
            notelist_ne[i * 24 + j] = bnotes[8]
        else:
            notelist_ne[i * 24 + j] = notelist_ne[i * 24 + j]


mixer = Mixer(44100, 0.5)
mixer.create_track(0, SINE_WAVE)
mixer.create_track(1, SINE_WAVE)
mixer.create_track(2, SINE_WAVE)
mixer.create_track(3, SINE_WAVE)
mixer.create_track(4, SINE_WAVE)
mixer.create_track(5, SINE_WAVE)
mixer.create_track(6, SINE_WAVE)
mixer.create_track(7, SINE_WAVE)
mixer.create_track(8, SINE_WAVE)

mixer.add_notes(0, notelist_sun)
mixer.add_notes(1, notelist_moon)
mixer.add_notes(2, notelist_me)
mixer.add_notes(3, notelist_ve)
mixer.add_notes(4, notelist_ma)
mixer.add_notes(5, notelist_ju)
mixer.add_notes(6, notelist_sa)
mixer.add_notes(7, notelist_ur)
mixer.add_notes(8, notelist_ne)

mixer.write_wav('planet_music.wav')
samples = mixer.mix()





# ### testing tone mixer
# # Create mixer, set sample rate and amplitude
# mixer = Mixer(44100, 0.5)

# #mary had a little lamb
# notelistn = [
#             ('e', 4, 0.5),
#             ('d', 4, 0.5),
#             ('c', 4, 0.5),
#             ('d', 4, 0.5),
#             ('e', 4, 0.5),
#             ('e', 4, 0.5),
#             ('e', 4, 1, 0, 0, 0, 0, 0),
#             ('d', 4, 0.5),
#             ('d', 4, 0.5),
#             ('d', 4, 1, None, None, None, None, 0),
#             ('e', 4, 0.5),
#             ('e', 4, 0.5),
#             ('e', 4, 1),
#             ]
# mixer.create_track(0, SINE_WAVE)

# # Add a 1-second tone on track 0, slide pitch from c# to f#)
# mixer.add_notes(0, notelistn)

# # Mix all tracks into a single list of samples and write to .wav file
# mixer.write_wav('tones.wav')

# # Mix all tracks into a single list of samples scaled from 0.0 to 1.0, and
# # return the sample list
# samples = mixer.mix()




