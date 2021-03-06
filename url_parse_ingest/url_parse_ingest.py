#
# (c) 2012 YourTrove, Inc. All Rights Reserved.
#

import sys
import urllib2
import settings
import tempfile
import simplejson as json
import parse_handler

class jsonDocument():

    def __init__(self, url, handlers=settings.MASTER_HANDLER):
        self._url = url

        # The bits we care about
        self._filetype = None
        self._title = None
        self._body = None
        self._ingested = None
        self._handlers = handlers

        # HTTP information
        self._content_length = None
        self._response = None
        self._data = None

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
        if not self._failed and not self._response:
            try:
                self._response = urllib2.urlopen(self._url)
                status = self._response.getcode()
                if status != 200:
                    # do the right thing
                    # account for redirects and try not to loop
                    pass
            except:
                self._failed = True
                self._debugPrint("_openURL() failed with unexpected error %s" % sys.exc_info()[0])

    def _loadHeaders(self):
        self._openURL()
        if not self._failed and self._response:
            headers = self._response.info()
            self._filetype = headers.get('content-type','unknown').split(';')[0]

    def _loadData(self):
        self._openURL()
        if not self._failed and self._response:
            try:
                self._data = tempfile.SpooledTemporaryFile(max_size=1048576)
                self._data.write(self._response.read())
                self._data.seek(0)
                self._ingested = True
                self._response.close()
            except:
                self.failed = True
                self._debugPrint("_loadData() unknown failure %s"  % sys.exc_info()[0])

    def setDebug(self, debug=True):
        self._DEBUG = debug
        message = "ENABLED" if debug else "DISABLED"
        print >> sys.stderr, "Debugging:", message

    def fetch(self):
        self._loadHeaders()
        self._loadData()

        if self._failed or not self._ingested:
            return json.dumps(settings.EMPTY_DATA)

        response = self._handlers.callHandler(self._filetype, self._data)

        return json.dumps(response)
