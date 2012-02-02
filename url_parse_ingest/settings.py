#
# (c) 2012 YourTrove, Inc. All Rights Reserved.
#

import re

EMPTY_DATA = {'title':'unknown', 'body':'unknown', 'content-length':'unknown'}

DEBUG = False

MASTER_HANDLER = None

TITLE_REGEX = re.compile("<title>(.[^<]*)</title>")

try:
    from local_settings import *    
except ImportError:
    pass
