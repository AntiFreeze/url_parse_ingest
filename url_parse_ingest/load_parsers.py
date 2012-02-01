import os, fnmatch
import settings
import parse_handler

if not settings.MASTER_HANDLER:
    settings.MASTER_HANDLER = parse_handler.registeredHandlers()

for file in os.listdir('.'):
    if fnmatch.fnmatch(file, 'parse_*'):
        if os.path.isdir(file):
            try:
                __import__(file)
            except:
                pass
