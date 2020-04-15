#!/usr/bin/python
# -*- coding: utf-8 -*-

import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import threading
import psutil
import threading
import time
import os
from sense_hat import SenseHat
from gpiozero import LED
from gpiozero import CPUTemperature

sense = SenseHat()
refresh_rate = 5

def on_connect(mqttc, obj, flags, rc):
    print("Connected with result code "+str(rc))
    mqttc.subscribe("/pi/led")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
        print(msg.topic+" "+str(msg.payload))
#        if msg.payload == "on":
#            green_led.on()
#        if msg.payload == "off":
#            green_led.off()

def on_publish(mqttc, obj, mid):
    print("mid: " + str(mid))


def on_subscribe(mqttc, obj, mid, granted_qos):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))


def on_log(mqttc, obj, level, string):
    print(string)

def ambiant_temp():
    while True:
        temp = sense.get_temperature()
        print("Ambiant temperature: %s °C" % temp)
        publish.single("/raspberry/ambiant_sensors/temp", temp, hostname="localhost")
        time.sleep(refresh_rate)

def ambiant_pressure():
    while True:
        pressure = sense.get_pressure()
        print("Ambiant pressure: %s Millibars" % pressure)
        publish.single("/raspberry/ambiant_sensors/pressure", pressure, hostname="localhost")
        time.sleep(refresh_rate)

def ambiant_humidity():
    while True:
        humidity = sense.get_humidity()
        print("Humidity: %s %%rH" % humidity)
        publish.single("/raspberry/ambiant_sensors/humidity", humidity, hostname="localhost")
        time.sleep(refresh_rate)

def cpu_temp():
    while True:
        cputemp = CPUTemperature()
        print("CPU temperature: %f °C" % cputemp.temperature)
#        if float(cputemp.temperature) < 50:
#            green_led.on()
#            red_led.off()
#        else:
#            green_led.off()
#            red_led.on()
        publish.single("/raspberry/cpu/temp", cputemp.temperature, hostname="localhost")
        time.sleep(refresh_rate)

def cpu_usage():
    while True:
        usage = psutil.cpu_percent(interval=0, percpu=False)
        print("CPU usage: %f %%" % usage)
        publish.single("/raspberry/cpu/usage", usage, hostname="localhost")
        time.sleep(refresh_rate)

# If you want to use a specific client id, use
# mqttc = mqtt.Client("client-id")
# but note that the client id must be unique on the broker. Leaving the client
# id parameter empty will generate a random id for you.
mqttc = mqtt.Client()
mqttc.on_message = on_message
mqttc.on_connect = on_connect
mqttc.on_publish = on_publish
mqttc.on_subscribe = on_subscribe
mqttc.connect("localhost", 1883, 60)
#try:
    # Uncomment to enable debug messages
    # mqttc.on_log = on_log
cpu_temp=threading.Thread(target=cpu_temp)
cpu_temp.daemon = True
cpu_temp.start()

cpu_usage=threading.Thread(target=cpu_usage)
cpu_usage.daemon = True
cpu_usage.start()

ambiant_temp=threading.Thread(target=ambiant_temp)
ambiant_temp.daemon = True
ambiant_temp.start()

ambiant_pressure=threading.Thread(target=ambiant_pressure)
ambiant_pressure.daemon = True
ambiant_pressure.start()

ambiant_humidity=threading.Thread(target=ambiant_humidity)
ambiant_humidity.daemon = True
ambiant_humidity.start()

mqttc.loop_forever()
#finally:
#    m.stop()
