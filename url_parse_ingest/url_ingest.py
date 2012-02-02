#
# (c) 2012 YourTrove, Inc. All Rights Reserved.
#

import re, sys, urllib2, tempfile
from pyPdf import PdfFileReader

DEBUG = False
EMPTY_DATA = {'title':'unknown', 'body':'unknown', 'content-length':'unknown'}
TITLE_REGEX = re.compile("<title>(.[^<]*)</title>")

def _debugPrint(message):
    if DEBUG:
        print >> sys.stderr, message

def loadDocument(url):
    try:
        response = urllib2.urlopen(url)
        status = response.getcode()
        if status != 200:
            _debugPrint("uh-oh, status: %s" % status)
            # do the right thing
            # account for redirects and try not to loop
            return EMPTY_DATA
    except:
        _debugPrint("error opening url %s: %s" % (url, sys.exc_info()[0]))
        return EMPTY_DATA

    try:
        headers = response.info()
        filetype = headers.get('content-type','unknown').split(';')[0]
    except:
        _debugPrint("url_ingest.loadDocument() error loading content type header: %s"  % sys.exc_info()[0])
        return EMPTY_DATA

    try:
        data = tempfile.SpooledTemporaryFile(max_size=1048576)
        data.write(response.read())
        data.seek(0)
        response.close()
    except:
        _debugPrint("url_ingest.loadDocument() unknown failure %s"  % sys.exc_info()[0])
        return EMPTY_DATA

    response = EMPTY_DATA
    try:
        if filetype == 'text/html':
            response = parse_html(data)
        elif filetype == 'application/pdf':
            response = parse_pdf(data)
        else:
            response.update({'body':data.read()})
        data.close()
    except:
        _debugPrint("url_ingest.loadDocument() unknown failure %s"  % sys.exc_info()[0])

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
        t = TITLE_REGEX.search(data)
        if t:
            return t.groups()[0]
        return None

    properties = {}

    try:
        value = stream.read()
    except:
        return EMPTY_DATA

    title = get_title(value)
    body = strip_script(value)
    body = strip_html(value)

    if title:
        properties.update({'title':title})
    properties.update({'body':body, 'content-length':len(body)})

    return properties
