# With apologies
__path__.append("..")

from settings import MASTER_HANDLER
import parse
import parse_handler

if not MASTER_HANDLER:
    MASTER_HANDLER = parse_handler.registeredHandlers()
MASTER_HANDLER.addHandler("application/pdf", parse.parse)
