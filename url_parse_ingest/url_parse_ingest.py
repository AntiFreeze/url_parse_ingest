import sys
import re, json
import urllib2

class jsonDocument():

    def __init__(self, url, fetch=True):
        self._url = url

        self._filetype = None
        self._title = None
        self._body = None
        self._parsed = None
        self._ingested = None
        self._response = None

        self._DEBUG = False

        if fetch:
            pass

    def _debugPrint(self, message):
        if self._DEBUG:
            print >> sys.stderr, message

    def setDebug(self, debug=True):
        self._DEBUG = debug
        message = "ENABLED" if debug else "DISABLED"
        print >> sys.stderr, "Debugging:", message

    def _getHeader(self):
        if not self._response:
            self._response = urllib2.urlopen(self._url)
        return self._response.info()
