import sys
import re, json
import urllib2

class registeredHandlers():
    def __init__(self):
        self._handlers = { 'unknown':self._unknown_handler }

    def __str__(self):
        message = "registeredHandlers(%d):" % len(self._handlers)
        for handler in self._handlers:
            message = message + handler
        return message

    def __repr__(self):
        message = "<url_parse_ingest.registeredHandlers(%d):" % len(self._handlers)
        for handler in self._handlers:
            message = message + " " + handler
        return message + ">"

    def _unknown_handler(self, data):
        return {'title':'unknown', 'body':'unknown', 'content-length':'unknown'}

    def isHandler(self, type):
        return True if type in self._hanlders else False

    def addHandler(self, type, func):
        if not self.isHandler(type):
            self._hanlders.update({type:func})
            return True
        return False

    def callHandler(self, type, data):
        if self.isHandler(type):
            return self._handlers[type](data)
        return {}

class jsonDocument():

    def __init__(self, url, handlers):
        self._url = url

        # The bits we care about
        self._filetype = None
        self._title = None
        self._body = None
        self._ingested = None
        self._handlers = handlers

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
        return "jsonDocument (ingested=%s) %s: type %s, title %s, size: %s" % (self._ingested, self._url, self._filetype, self._title, self._content_length)

    def __repr__(self):
        return "<url_parse_ingest.jsonDocument ingested=%s, url=%s: type %s, title %s, size: %s>" % (self._ingested, self._url, self._filetype, self._title, self._content_length)

    def _debugPrint(self, message):
        if self._DEBUG:
            print >> sys.stderr, message

    def _openURL(self):
        if not self._response:
            try:
                self._response = urllib2.urlopen(self._url)
                if self._response.status != 200:
                    # do the right thing
                    # account for redirects and try not to loop
                    pass
            except:
                self._failed = True
                self._debugPrint("_openURL() failed with unexpected error %s" % sys.exc_info()[0])

    def _getHeaders(self):
        headers = []
        self._openURL()
        if not self._response:
            headers = self._response.info()
            content_type = headers.get('content-type','unknown;unknown').split(';')
            self._content_length = headers.get('content-length',0)
            self._filetype = content_type[0]
            self._charset = content_type[1]
            self._debugPrint("_getHeader(%s): filetype: %s, charset: %s, length: %s" % (self._url, self._filetype, self._charset, self._content_length))

        return headers

    def setDebug(self, debug=True):
        self._DEBUG = debug
        message = "ENABLED" if debug else "DISABLED"
        print >> sys.stderr, "Debugging:", message

    def fetch(self):
        self._getHeaders()
        if not self._response:
            return {}

        response = self._handlers.callHandler(self._filetype)

        return response
