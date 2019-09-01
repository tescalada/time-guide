import urequests as requests
import math
import gc

long_i = [200.0, 48.0, 126.0, 260.0, 286.0, 33.0, 346.0]
years_i = ['August 20, 2019', 'August 8, 2019', 'August 3, 2020', 'January 24, 2023', 'December 24, 2032', 'February 10, 2051', 'July 16, 2047']
longp_i = [76.0, 131.0, 336.0, 14.0, 93.0, 173.0, 49.0]
period_i = [0.2408467, 0.61519726, 1.8808476, 11.862615, 29.447498, 84.016846, 164.79132]
dist_i = [0.928, 1.65, 2.51, 4.29, 9.1, 20.5, 29.8]
sdist_i = [0.417, 0.723, 1.64, 5.3, 10.1, 19.8, 29.9]

def getOrbitData(names, WOLFRAM_API_KEY):

    # earth heliocentric longitude
    url = "http://api.wolframalpha.com/v1/result?i=earth%20heliocentric%20longitude%3F&appid={0}".format(WOLFRAM_API_KEY)
    r = requests.get(url)
    print(r.text)
    elong = [x.strip() for x in r.text.split(',')]
    elong = [x.strip() for x in elong[0].split()]
    elong = elong[0]
    r.close()
    del r
    print(elong)
    elong = float(elong)
    elong = math.radians(elong)

    for index, name in enumerate(names):
        #oled stuff
        oled.fill(0)
        oled.text("getting:", 0, 0)
        oled.text(name, 0, 10)
        oled.show()
        utime.sleep(1)

        # heliocentric longitude
        url = "http://api.wolframalpha.com/v1/result?i={0}%20heliocentric%20longitude%3F&appid={1}".format(name, WOLFRAM_API_KEY)
        r = requests.get(url)
        print(r.text)
        long = [x.strip() for x in r.text.split(',')]
        long = [x.strip() for x in long[0].split()]
        long = long[0]
        r.close()
        del r
        print(long)
        # save planet data to list
        long_i[index] = float(long)

        # perihelion data
        url = "http://api.wolframalpha.com/v1/result?i={0}%20next%20periapsis%3F&appid={1}".format(name, WOLFRAM_API_KEY)
        r = requests.get(url)
        print(r.text)
        years = r.text
        years = [x.strip() for x in years.split()]
        years = years[0][:3] + " " + years[1] + " " + years[2]
        r.close()
        del r
        gc.collect()
        # save planet data to list
        years_i[index] = years

        # heliocentric longitude @ next perihelion
        url = "http://api.wolframalpha.com/v1/result?i={0}%20heliocentric%20longitude%20at%20next%20perihelion%3F&appid={1}".format(name, WOLFRAM_API_KEY)
        r = requests.get(url)
        print(r.text)
        longp = [x.strip() for x in r.text.split(',')]
        longp = [x.strip() for x in longp[0].split()]
        longp = longp[0]
        r.close()
        del r
        print(longp)
        # save planet data to list
        longp_i[index] = float(longp)

        # orbital period data from wolframalpha API
        url = "http://api.wolframalpha.com/v1/result?i={0}%20orbital%20period%20in%20julian%20years%3F&appid={1}".format(name, WOLFRAM_API_KEY)
        r = requests.get(url)
        print(r.text)
        period = [x.strip() for x in r.text.split()]
        period = period[0]
        print(period)
        r.close()
        del r
        gc.collect()
        # save planet data to list
        period_i[index] = float(period)

        # distance from earth
        url = "http://api.wolframalpha.com/v1/result?i={0}%20distance%20from%20earth%3F&appid={1}".format(name, WOLFRAM_API_KEY)
        r = requests.get(url)
        print(r.text)
        dist = [x.strip() for x in r.text.split(',')]
        dist = [x.strip() for x in dist[0].split()]
        dist = dist[1]
        r.close()
        del r
        gc.collect()
        print(dist)
        # save planet data to list
        dist_i[index] = float(dist)

        #oled stuff
        oled.fill(0)
        oled.text(name, 0, 0)
        oled.text("acquired!", 0, 10)
        oled.show()
        utime.sleep(1)

visible_i = [0, 0, 0, 0, 0, 0, 0]  # currently above horizon
alc_i = [0, 0, 0, 0, 0, 0, 0]  # current altitude
alm_i = [0, 0, 0, 0, 0, 0, 0]  # maximum altitude
azc_i = [0, 0, 0, 0, 0, 0, 0]  # current azimuth
azr_i = [0, 0, 0, 0, 0, 0, 0]  # azimuth at planet rise
azs_i = [0, 0, 0, 0, 0, 0, 0]  # aximuth at planet set
azm_i = [0, 0, 0, 0, 0, 0, 0]  # azimuth at maximum altitude

def getSkychartData(names, WOLFRAM_API_KEY):

    for index, name in enumerate(names):
        #oled stuff
        oled.fill(0)
        oled.text("getting:", 0, 0)
        oled.text(name, 0, 10)
        oled.show()
        utime.sleep(1)

        # obtain planet above horizon from wolframalpha API
        url = "http://api.wolframalpha.com/v1/result?i={0}%20above%20horizon%3F&appid={1}".format(name, WOLFRAM_API_KEY)
        r = requests.get(url)
        print(r.text)
        visible = [x.strip() for x in r.text.split(',')]
        visible = visible[0]
        print(visible)
        r.close()
        del r
        gc.collect()
        # save planet data to list
        visible_i[index] = visible

        # sky chart data
        # obtain current planet azimuth from wolframalpha API
        url = "http://api.wolframalpha.com/v1/result?i={0}%20azimuth%3F&appid={1}".format(name, WOLFRAM_API_KEY)
        r = requests.get(url)
        print(r.text)
        azc = [x.strip() for x in r.text.split(',')]
        azc = [x.strip() for x in azc[0].split()]
        azc = azc[0]
        azc = float(azc)
        print(azc)
        r.close()
        del r
        gc.collect()
        # save planet data to list
        azc_i[index] = azc

        # obtain planet azimuth rise from wolframalpha API
        url = "http://api.wolframalpha.com/v1/result?i={0}%20azimuth%20rise%3F&appid={1}".format(name, WOLFRAM_API_KEY)
        r = requests.get(url)
        print(r.text)
        azr = [x.strip() for x in r.text.split(',')]
        azr = [x.strip() for x in azr[0].split()]
        azr = azr[0]
        azr = float(azr)
        print(azr)
        r.close()
        del r
        gc.collect()
        # save planet data to list
        azr_i[index] = azr

        # obtain planet azimuth set from wolframalpha API
        url = "http://api.wolframalpha.com/v1/result?i={0}%20azimuth%20set%3F&appid={1}".format(name, WOLFRAM_API_KEY)
        r = requests.get(url)
        print(r.text)
        azs = [x.strip() for x in r.text.split(',')]
        azs = [x.strip() for x in azs[0].split()]
        azs = azs[0]
        azs = float(azs)
        print(azs)
        r.close()
        del r
        gc.collect()
        # save planet data to list
        azs_i[index] = azs

        # obtain planet azimuth at maximum altitude from wolframalpha API
        url = "http://api.wolframalpha.com/v1/result?i={0}%20azimuth%20at%20time%20of%20maximum%20altitude%3F&appid={1}".format(name, WOLFRAM_API_KEY)
        r = requests.get(url)
        print(r.text)
        azm = [x.strip() for x in r.text.split(',')]
        azm = [x.strip() for x in azm[0].split()]
        azm = azm[0]
        azm = float(azm)
        print(azm)
        r.close()
        del r
        gc.collect()
        # save planet data to list
        azm_i[index] = azm

        # obtain current planet altitude from wolframalpha API
        url = "http://api.wolframalpha.com/v1/result?i={0}%20altitude%3F&appid={1}".format(name, WOLFRAM_API_KEY)
        r = requests.get(url)
        print(r.text)
        alc = [x.strip() for x in r.text.split(',')]
        alc = [x.strip() for x in alc[0].split()]
        alc = alc[0]
        alc = float(alc)
        print(alc)
        r.close()
        del r
        gc.collect()
        # save planet data to list
        alc_i[index] = alc

        # obtain max planet altitude from wolframalpha API
        url = "http://api.wolframalpha.com/v1/result?i={0}%20maximum%20altitude%3F&appid={1}".format(name, WOLFRAM_API_KEY)
        r = requests.get(url)
        print(r.text)
        alm = [x.strip() for x in r.text.split(',')]
        alm = [x.strip() for x in alm[0].split()]
        alm = alm[0]
        alm = float(alm)
        print(alm)
        r.close()
        del r
        gc.collect()
        # save planet data to list
        alm_i[index] = alm

        #oled stuff
        oled.fill(0)
        oled.text(name, 0, 0)
        oled.text("acquired!", 0, 10)
        oled.show()
        utime.sleep(1)


