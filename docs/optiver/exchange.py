from optibook.synchronous_client import Exchange
import logging

exchange = Exchange()
exchange.connect()
logging.getLogger("client").setLevel("ERROR")
