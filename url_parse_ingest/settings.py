#
# (c) 2012 YourTrove, Inc. All Rights Reserved.
#

EMPTY_DATA = {'title':'unknown', 'body':'unknown', 'content-length':'unknown'}

DEBUG = False

#Mutable!
MASTER_HANDLER = None

try:
    from local_settings import *    
except ImportError:
    pass
