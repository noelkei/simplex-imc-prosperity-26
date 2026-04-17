import threading
import time
import sys
import logging

logging.getLogger("client").setLevel("ERROR")

from asml_bot import run_asml_bot
from tesla_bot import TSLA_MM
from arbitrage import arbitrage
from futures import futures

def run_asml():
    print("ASML STARTED")
    run_asml_bot()

def run_tsla():
    print("TSLA STARTED")
    TSLA_MM()

def arbitrage_thread():
    print("SAP STARTED")
    arbitrage()

def futures_thread():
    print("FUTURES STARTED")
    futures()

if __name__ == "__main__":
    t1 = threading.Thread(target=run_asml, daemon=True) # 100/min
    t2 = threading.Thread(target=run_tsla, daemon=True) # 300/min
    t3 = threading.Thread(target=arbitrage_thread, daemon=True)
    t4 = threading.Thread(target=futures_thread, daemon=True) # 300/min

    t2.start()
    time.sleep(1)   # stagger para evitar burst
    t4.start()
    time.sleep(1)
    t1.start()
    # time.sleep(1)   # stagger para evitar burst
    # t3.start()

    try:
        while True:
            time.sleep(0.5)

    except Exception as e:
        print("\n🛑 SHUTDOWN")
        sys.exit(0)