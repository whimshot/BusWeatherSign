"""A simple claass for weather data."""
import pywapi
import threading
import time

DEBUG = False


class weather:
    """A simple claass for weather data."""

    forecast = ''
    interval = 300  # Default polling interval = 5 minutes
    initSleep = 0   # Stagger polling threads to avoid load spikes
    error = ''

    def __init__(self, station):
        """Setup weather object instance."""
        self.station = station
        self.lastQueryTime = time.time()
        t = threading.Thread(target=self.thread)
        t.daemon = True
        t.start()

    def thread(self):
        """Thread for querying the weather."""
        initSleep = weather.initSleep
        weather.initSleep += 5
        time.sleep(initSleep)
        while True:
            try:
                noaa_result = pywapi.get_weather_from_noaa(self.station)
                self.forecast = noaa_result['temp_c'] + " C. " + \
                    noaa_result['weather']
                if DEBUG:
                    print "Forecast retrieved: %s" % self.forecast
            except Exception:
                self.forecast = "Failed to get forecast."
                if DEBUG:
                    print "Failed to get forecast."
            finally:
                time.sleep(weather.interval)
