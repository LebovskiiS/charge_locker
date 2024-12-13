import logging
from logging import StreamHandler, Formatter
import sys

handler = StreamHandler(sys.stdout)
formater = Formatter(fmt='%(asctime)s, %(funcName)s, %(filename)s, %(message)s')
logger = logging.getLogger(__name__)

handler.setLevel(logging.DEBUG)
handler.setFormatter(formater)
logger.setLevel(logging.DEBUG)
logger.addHandler(handler)




