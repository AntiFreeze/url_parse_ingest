import sys
import re, json
import urllib2

class jsonDocument():

    def __init__(self, url):
        self._url = url

        # The bits we care about
        self._filetype = None
        self._title = None
        self._body = None
        self._ingested = None

        # HTTP information
        self._content_length = None
        self._content_charset = None
        self._response = None

        # Post-parsing information
        self._parsed_length = None

        # Helpers
        self._failed = False
        self._DEBUG = False

    def __del__(self):
        if self._response:
            self._response.close()

    def __str__(self):
        return "jsonDocument (ingested=%s) %s: type %s, title %s, size: %d" % (self._ingested, self._url, self._filetype, self._title, self._content_length)

    def __repr__(self):
        return "<url_parse_ingest.jsonDocument ingested=%s, url=%s: type %s, title %s, size: %d>" % (self._ingested, self._url, self._filetype, self._title, self._content_length)

    def _debugPrint(self, message):
        if self._DEBUG:
            print >> sys.stderr, message

    def _getHeaders(self):
        headers = []
        if not self._response:
            try:
                self._response = urllib2.urlopen(self._url)
                headers = self._response.info()
                content_type = headers['content-type'].split(';')
                self._content_length = headers['content-length']
                self._filetype = content_type[0]
                self._charset = content_type[1]
                self._debugPrint("_getHeader(%s): filetype: %s, charset: %s, length: %s", self._filetype, self._charset, self._content_length)
            except:
                self._failed = True
                self._debugPrint("_getHeader() failed with unexpected error %s" % sys.exc_info()[0])

        return headers

    def setDebug(self, debug=True):
        self._DEBUG = debug
        message = "ENABLED" if debug else "DISABLED"
        print >> sys.stderr, "Debugging:", message

    def fetch(self):
        self._getHeaders()
        if not self._response:
            # yuh-oh
            return {}

        if self._filetype == "text/html":
            pass
        elif self._filetype == "text/pdf":
            pass
        elif self._filetype == "text/docx":
            pass

        return {}
