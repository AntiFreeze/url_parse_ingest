#
# (c) 2012 YourTrove, Inc. All Rights Reserved.
#

import settings

class registeredHandlers():
    def __init__(self):
        self._handlers = { 'unknown':self._unknown_handler }

    def __str__(self):
        message = "registeredHandlers(%d):" % len(self._handlers)
        for handler in self._handlers:
            message = message + " " + handler
        return message

    def __repr__(self):
        message = "<url_parse_ingest.registeredHandlers(%d):" % len(self._handlers)
        for handler in self._handlers:
            message = message + " " + handler
        return message + ">"

    def _unknown_handler(self, stream):
        response = settings.EMPTY_DATA
        try:
            body = stream.read()
        except:
            body = ""
        response.update({'body':body, 'content-length':len(body)})
        return response

    def isHandler(self, type):
        return True if type in self._handlers else False

    def addHandler(self, type, func):
        if not self.isHandler(type):
            self._handlers.update({type:func})
            return True
        return False

    def callHandler(self, type, stream):
        if self.isHandler(type):
            return self._handlers[type](stream)
        return self._handlers['unknown'](stream)
