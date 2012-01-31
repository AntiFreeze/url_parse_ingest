import re, json
import urllib, urllib2

class jsonDocument():

    def __init__(self, url):
        self._url = url

        self._filetype = None
        self._title = None
        self._body = None
        self._parsed = None
        self._ingested = None

        self._DEBUG = False

    def getHeader(self):
        pass
