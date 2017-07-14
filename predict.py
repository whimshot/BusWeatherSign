"""
NextBus prediction class.

For each route/stop, NextBus server is polled automatically at regular
intervals. Front-end app just needs to init this with stop data, which can be
found using the routefinder.py script.
"""
import threading
import time
import urllib
from xml.dom.minidom import parseString


class predict:
    """Predict object class."""
    interval = 120  # Default polling interval = 2 minutes
    initSleep = 0   # Stagger polling threads to avoid load spikes

    def __init__(self, data):
        """
        Predict object initializer.

        1 parameter, a 4-element tuple:

        First element is agengy tag (e.g. 'actransit')

        Second is line tag (e.g. '210')

        Third is stop tag (e.g. '0702630')

        Fourth is direction -- not a tag, this element is human-readable and
        editable (e.g. 'Union Landing') -- for UI purposes you may want to keep
        this short.  The other elements MUST be kept verbatim as displayed by
        the routefinder.py script. Each predict object spawns its own thread
        and will perform periodic server queries in the background, which can
        then be read via the predictions[] list (est. arrivals, in seconds).

        """
        self.data = data
        self.predictions = []
        self.lastQueryTime = time.time()
        t = threading.Thread(target=self.thread)
        t.daemon = True
        t.start()

    def thread(self):
        """Thread to query for predictions."""
        initSleep = predict.initSleep
        predict.initSleep += 5   # Thread staggering may
        time.sleep(initSleep)    # drift over time, no problem
        while True:
            dom = predict.req('predictions' +
                              '&a=' + self.data[0] +   # Agency
                              # '&r=' + self.data[1] +   # Route
                              '&stopId=' + self.data[2])    # Stop
            if dom is None:
                return     # Connection error
            self.lastQueryTime = time.time()
            predictions = dom.getElementsByTagName('prediction')
            newList = []
            for p in predictions:      # Build new prediction list
                newList.append(
                    int(p.getAttribute('seconds')))
            newList_set = set(newList)  # Replace current list
            self.predictions = sorted(newList_set)  # Replace current list
            time.sleep(predict.interval)

    @staticmethod
    def req(cmd):
        """Open URL, send request, read & parse XML response."""
        xml = None
        try:
            connection = urllib.urlopen(
                'http://webservices.nextbus.com' +
                '/service/publicXMLFeed?command=' + cmd)
            raw = connection.read()
            connection.close()
            xml = parseString(raw)
        finally:
            return xml

    @staticmethod
    def setInterval(i):
        """Set polling interval (seconds)."""
        interval = i
