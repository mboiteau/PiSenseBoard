# -*- coding: utf-8 -*-
from sense_hat import SenseHat
import psutil
import paho.mqtt.publish as publish
from gpiozero import CPUTemperature

sense = SenseHat()

class Utility:

    def rgb_parsing(rgb_result):
        parsed = (rgb_result.replace(" ", "")).split(',')
        rgb_array = []
        for i in parsed:
            s = ''.join([c for c in i if c.isdigit()])
            rgb_array.append(int(s))
        return rgb_array

    @staticmethod
    def led_func(topic, data):
        if topic == "/raspberry/led/luminosity":
            if data == "1":
                print("low light off")
                sense.low_light = False
            if data == "0":
                print("low light on")
                sense.low_light = True
        if topic == "/raspberry/led/state":
            if data == "True":
                print("led state on")
                sense.clear(255,255,255)
            if data == "False":
                print("led state off")
                sense.clear()
        if topic == "/raspberry/led/color":
            rgb_array = rgb_parsing(msg.payload)
            sense.clear(rgb_array[0], rgb_array[1], rgb_array[2])

    @staticmethod
    def ambiant_temp():
        temp = sense.get_temperature()
        print("Ambiant temperature: %s °C" % temp)
        publish.single("/raspberry/ambiant_sensors/temp", temp, hostname="localhost")

    @staticmethod
    def ambiant_pressure():
        pressure = sense.get_pressure()
        print("Ambiant pressure: %s Millibars" % pressure)
        publish.single("/raspberry/ambiant_sensors/pressure", pressure, hostname="localhost")

    @staticmethod
    def ambiant_humidity():
        humidity = sense.get_humidity()
        print("Humidity: %s %%rH" % humidity)
        publish.single("/raspberry/ambiant_sensors/humidity", humidity, hostname="localhost")

    @staticmethod
    def cpu_temp():
        cputemp = CPUTemperature()
        print("CPU temperature: %f °C" % cputemp.temperature)
        publish.single("/raspberry/cpu/temp", cputemp.temperature, hostname="localhost")
        #        if float(cputemp.temperature) < 50:
        #            green_led.on()
        #            red_led.off()
        #        else:
        #            green_led.off()
        #            red_led.on()

    @staticmethod
    def cpu_usage():
        usage = psutil.cpu_percent(interval=0, percpu=False)
        print("CPU usage: %f %%" % usage)
        publish.single("/raspberry/cpu/usage", usage, hostname="localhost")
