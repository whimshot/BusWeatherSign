#!/usr/bin/python

import pywapi
import threading
import time


class weather:

    forecast = ''
    interval = 300  # Default polling interval = 5 minutes
    initSleep = 0   # Stagger polling threads to avoid load spikes

    def __init__(self, station):
        self.station = station
        self.lastQueryTime = time.time()
        t = threading.Thread(target=self.thread)
        t.daemon = True
        t.start()

    def thread(self):
        initSleep = weather.initSleep
        weather.initSleep += 5
        time.sleep(initSleep)
        while True:
            try:
                print "Getting weather forcast\n"
                noaa_result = pywapi.get_weather_from_noaa(self.station)
                self.forecast = noaa_result['temp_c'] + " C. " + \
                    noaa_result['weather']
                print "Got %s" % self.forecast
            except error:
                self.forecact = "Failed to get forecast."
                print "Failed to get forecast.\n"
            time.sleep(weather.interval)
