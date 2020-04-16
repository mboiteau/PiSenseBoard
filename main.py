#!/usr/bin/python
# -*- coding: utf-8 -*-

import threading
import time
from Client import Client
from Utility import Utility

def thread_pool():
    refresh_rate = 5
    
    while True:
        cpu_temp_thread=threading.Thread(target=Utility.cpu_temp)
        cpu_temp_thread.start()
        time.sleep(0.05)
        cpu_usage_thread=threading.Thread(target=Utility.cpu_usage)
        cpu_usage_thread.start()
        time.sleep(0.05)
        ambiant_temp_thread=threading.Thread(target=Utility.ambiant_temp)
        ambiant_temp_thread.start()
        time.sleep(0.05)
        ambiant_pressure_thread=threading.Thread(target=Utility.ambiant_pressure)
        ambiant_pressure_thread.start()
        time.sleep(0.05)
        ambiant_humidity_thread=threading.Thread(target=Utility.ambiant_humidity)
        ambiant_humidity_thread.start()
        time.sleep(refresh_rate)
        print("\n")

def main():
    client = Client()
    client.connect()
    main_thread=threading.Thread(target=thread_pool)
    main_thread.daemon = True
    main_thread.start()
    client.start()

if __name__ == "__main__":
    main()
