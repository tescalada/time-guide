import requests
import datetime
from credentials import WOLFRAM_API_KEY

from tones import SINE_WAVE
from tones.mixer import Mixer

notelistn = [
            ('e', 4, 0.5),
            ('d', 4, 0.5),
            ('c', 4, 0.5),
            ('d', 4, 0.5),
            ('e', 4, 0.5),
            ('e', 4, 0.5),
            ('e', 4, 1),
            ('d', 4, 0.5),
            ('d', 4, 0.5),
            ('d', 4, 1),
            ('e', 4, 0.5),
            ('e', 4, 0.5),
            ('e', 4, 1),
            ]


# Create mixer, set sample rate and amplitude
mixer = Mixer(44100, 0.5)

# Create two monophonic tracks that will play simultaneously, and set
# initial values for note attack, decay and vibrato frequency (these can
# be changed again at any time, see documentation for tones.Mixer
mixer.create_track(0, SINE_WAVE)

# Add a 1-second tone on track 0, slide pitch from c# to f#)
mixer.add_notes(0, notelistn)

# Mix all tracks into a single list of samples and write to .wav file
mixer.write_wav('tones.wav')

# Mix all tracks into a single list of samples scaled from 0.0 to 1.0, and
# return the sample list
samples = mixer.mix()


## get rise/set times as strings from wolframalpha API

# days = 2
# date = datetime.datetime(2021,3,21)
# names = ['Sun', 'Moon', 'Mercury', 'Venus', 'Mars', 'Jupiter', 'Saturn', 'Uranus', 'Neptune']
# rise = [[0 for i in range(len(names))] for j in range(days)]
# sett = [[0 for i in range(len(names))] for j in range(days)]


# for index1 in range(days):
#     for index2, name in enumerate (names) :

#         # obtain  rise time from wolframalpha API
#         url = "http://api.wolframalpha.com/v1/result?i={0}%20rise%20{1}%3F&appid={2}".format(name, date, WOLFRAM_API_KEY)
#         r = requests.get(url)
#         print(r.text)
#         rise[index1][index2] = r.text
#         r.close()
#         del r

#         # obtain set time from wolframalpha API
#         url = "http://api.wolframalpha.com/v1/result?i={0}%20set%20{1}%3F&appid={2}".format(name, date, WOLFRAM_API_KEY)
#         r = requests.get(url)
#         print(r.text)
#         sett[index1][index2] = r.text
#         r.close()
#         del r
#     date += datetime.timedelta(days=1)


