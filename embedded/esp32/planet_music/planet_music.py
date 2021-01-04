import requests
import datetime
from music import *
from credentials import WOLFRAM_API_KEY



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


