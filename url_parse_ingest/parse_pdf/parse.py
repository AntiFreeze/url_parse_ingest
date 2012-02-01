from pyPdf import PdfFileReader

def parse(data):
    properties = {}
    body = ""
    document = PdfFileReader(data)

    if document.isEncrypted:
        return {'encrypted':True}
    if 'Title' in document.documentInfo:
        properties.update({'title':document.documentInfo['Title']})

    for page in document.pages:
        body = body + "\n" +  page.extractText()

    properties.update({'body':body})

    return properties
