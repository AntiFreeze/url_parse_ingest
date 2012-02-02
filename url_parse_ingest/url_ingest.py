#
# (c) 2012 YourTrove, Inc. All Rights Reserved.
#

import settings
import parse_handler
import re, sys, urllib2, tempfile
from pyPdf import PdfFileReader

def _debugPrint(message):
    if settings.DEBUG:
        print >> sys.stderr, message

def loadDocument(url):
    if not settings.MASTER_HANDLER:
        handler_setup()

    try:
        response = urllib2.urlopen(url)
        status = response.getcode()
        if status != 200:
            _debugPrint("uh-oh, status: %s" % status)
            # do the right thing
            # account for redirects and try not to loop
            return settings.EMPTY_DATA
    except:
        _debugPrint("error opening url %s: %s" % (url, sys.exc_info()[0]))
        return settings.EMPTY_DATA

    headers = response.info()
    filetype = headers.get('content-type','unknown').split(';')[0]

    try:
        data = tempfile.SpooledTemporaryFile(max_size=1048576)
        data.write(response.read())
        data.seek(0)
        response.close()
    except:
        _debugPrint("_loadData() unknown failure %s"  % sys.exc_info()[0])
        return settings.EMPTY_DATA

    try:
        response = settings.MASTER_HANDLER.callHandler(filetype, data)
        data.close()
    except:
        response = settings.EMPTY_DATA

    return response

def parse_pdf(stream):
    properties = {}
    body = ""
    document = PdfFileReader(stream)

    if document.isEncrypted:
        return {'encrypted':True}
    if 'Title' in document.documentInfo:
        properties.update({'title':document.documentInfo['Title']})

    for page in document.pages:
        body = body + "\n" +  page.extractText()

    properties.update({'body':body, 'content-length':len(body)})

    return properties

def parse_html(stream):

    def strip_html(data):
        return re.sub(r'<[^>]*?>', '', data)

    def strip_script_ugly(data):
        abspos = 0
        stripped = ""

        result = re.search(r'<script', data)
        if not result:
            return data

        while result:
            stripped = stripped + data[abspos:abspos+result.start()]

            result = re.search(r'</script>', data[abspos:])
            if result:
                abspos = abspos+result.end()
                result = re.search(r'<script', data[abspos:])

        return stripped

    def strip_script(data):
        return re.sub(r'<script[^>]*?>[^<]*?</script>', '', data)

    def get_title(data):
        t = settings.TITLE_REGEX.search(data)
        if t:
            return t.groups()[0]
        return None

    properties = {}

    try:
        value = stream.read()
    except:
        return settings.EMPTY_DATA

    title = get_title(value)
    body = strip_script(value)
    body = strip_html(value)

    if title:
        properties.update({'title':title})
    properties.update({'body':body, 'content-length':len(body)})

    return properties

def handler_setup():
    if not settings.MASTER_HANDLER:
        settings.MASTER_HANDLER = parse_handler.registeredHandlers()
        settings.MASTER_HANDLER.addHandler("text/html", parse_html)
        settings.MASTER_HANDLER.addHandler("application/pdf", parse_pdf)
