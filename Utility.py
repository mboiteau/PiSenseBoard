# -*- coding: utf-8 -*-
from sense_hat import SenseHat
import psutil
import time
import threading
import paho.mqtt.publish as publish
from gpiozero import CPUTemperature

sense = SenseHat()

class Utility:
    temp = 0
    pressure = 0
    humidity = 0
    cputemp = 0
    usage = 0
    pixels = None
    mode_activated = False
    static_clr_activated = False
    current_thread = None
    
    @staticmethod
    def rgb_parsing(rgb_result):
        parsed = (rgb_result.replace(" ", "")).split(',')
        rgb_array = []
        for i in parsed:
            s = ''.join([c for c in i if c.isdigit()])
            rgb_array.append(int(s))
        return rgb_array

    @staticmethod
    def led_mode_selector(mode):
        if mode == "0":
            Utility.current_thread=threading.Thread(target=Utility.rainbow_mode)
            Utility.current_thread.start()
        if mode == "1":
            Utility.current_thread=threading.Thread(target=Utility.strombo_mode)
            Utility.current_thread.start()
        if mode == "2":
            Utility.current_thread=threading.Thread(target=Utility.color_mode)
            Utility.current_thread.start()
        if mode == "3":
            Utility.current_thread=threading.Thread(target=Utility.display_text_mode)
            Utility.current_thread.start()

    @staticmethod
    def next_colour(pix):
        r = pix[0]
        g = pix[1]
        b = pix[2]

        if (r == 255 and g < 255 and b == 0):
            g += 1
        if (g == 255 and r > 0 and b == 0):
            r -= 1
        if (g == 255 and b < 255 and r == 0):
            b += 1
        if (b == 255 and g > 0 and r == 0):
            g -= 1
        if (b == 255 and r < 255 and g == 0):
            r += 1
        if (r == 255 and b > 0 and g == 0):
            b -= 1

        pix[0] = r
        pix[1] = g
        pix[2] = b

    @staticmethod
    def display_text_mode():
        t = threading.currentThread()
        while getattr(t, "do_run", True):
            s = "Temp CPU: "+str(round(Utility.temp,1))+" CPU usage: "+str(Utility.usage)
            sense.show_message(s, text_colour=[255, 0, 0])

    @staticmethod
    def strombo_mode():
        pixels_strombo = []
        for i in range(0, 64):
            pixels_strombo.append([252, 248, 252])
        print(pixels_strombo)
        sense.set_pixels(pixels_strombo)
        msleep = lambda x: time.sleep(x / 1000.0)
        t = threading.currentThread() 
        while getattr(t, "do_run", True):
            sense.set_pixels(pixels_strombo)
            msleep(50)
            sense.clear()
            msleep(50)

    @staticmethod
    def color_mode():
        msleep = lambda x: time.sleep(x / 1000.0)
        t = threading.currentThread()
        r, g, b, i = 0, 0, 0, 0
        while getattr(t, "do_run", True):
            if i == 0:
                r = 255
                g = 0
                b = 0
            if i == 1:
                r = 0
                g = 255
                b = 0
            if i == 3:
                r = 0
                g = 0
                b = 255
                i = 0
            else:
                i = i + 1
            sense.clear(r,g,b)
            msleep(500)

    @staticmethod
    def rainbow_mode():
        pixels_rainbow = [
            [255, 0, 0], [255, 0, 0], [255, 87, 0], [255, 196, 0], [205, 255, 0], [95, 255, 0], [0, 255, 13], [0, 255, 122],
            [255, 0, 0], [255, 96, 0], [255, 205, 0], [196, 255, 0], [87, 255, 0], [0, 255, 22], [0, 255, 131], [0, 255, 240],
            [255, 105, 0], [255, 214, 0], [187, 255, 0], [78, 255, 0], [0, 255, 30], [0, 255, 140], [0, 255, 248], [0, 152, 255],
            [255, 223, 0], [178, 255, 0], [70, 255, 0], [0, 255, 40], [0, 255, 148], [0, 253, 255], [0, 144, 255], [0, 34, 255],
            [170, 255, 0], [61, 255, 0], [0, 255, 48], [0, 255, 157], [0, 243, 255], [0, 134, 255], [0, 26, 255], [83, 0, 255],
            [52, 255, 0], [0, 255, 57], [0, 255, 166], [0, 235, 255], [0, 126, 255], [0, 17, 255], [92, 0, 255], [201, 0, 255],
            [0, 255, 66], [0, 255, 174], [0, 226, 255], [0, 117, 255], [0, 8, 255], [100, 0, 255], [210, 0, 255], [255, 0, 192],
            [0, 255, 183], [0, 217, 255], [0, 109, 255], [0, 0, 255], [110, 0, 255], [218, 0, 255], [255, 0, 183], [255, 0, 74]
        ]

        msleep = lambda x: time.sleep(x / 1000.0)
        t = threading.currentThread()
        while getattr(t, "do_run", True):
            for pix in pixels_rainbow:
                Utility.next_colour(pix)

            sense.set_pixels(pixels_rainbow)
            msleep(2)
        sense.clear()

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
                Utility.static_clr_activated = True
                Utility.mode_activated = False
                sense.set_pixels(Utility.pixels)
            if data == "False":
                print("led state off\n")
                Utility.static_clr_activated = False
                Utility.pixels = sense.get_pixels()
                print(Utility.pixels)
                sense.clear()
        if topic == "/raspberry/led/color" and Utility.static_clr_activated == True:
            print(data)
            rgb_array = Utility.rgb_parsing(data)
            sense.clear(rgb_array[0], rgb_array[1], rgb_array[2])
        if topic == "/raspberry/led/mode/activate":
            if data == "True":
                Utility.mode_activated = True
                Utility.static_clr_activated = False
                Utility.led_mode_selector("0")
            if data == "False":
                Utility.current_thread.do_run = False
                Utility.current_thread.join()
                sense.set_pixels(Utility.pixels)
                Utility.mode_activated = False
        if topic == "/raspberry/led/mode" and Utility.mode_activated == True:
            if Utility.current_thread is not None:
                Utility.current_thread.do_run = False
                Utility.current_thread.join()
            Utility.led_mode_selector(data)

    @staticmethod
    def ambiant_temp():
        Utility.temp = sense.get_temperature()
        print("Ambiant temperature: %s °C" % Utility.temp)
        publish.single("/raspberry/ambiant_sensors/temp", Utility.temp, hostname="localhost")

    @staticmethod
    def ambiant_pressure():
        Utility.pressure = sense.get_pressure()
        print("Ambiant pressure: %s Millibars" % Utility.pressure)
        publish.single("/raspberry/ambiant_sensors/pressure", Utility.pressure, hostname="localhost")

    @staticmethod
    def ambiant_humidity():
        Utility.humidity = sense.get_humidity()
        print("Humidity: %s %%rH" % Utility.humidity)
        publish.single("/raspberry/ambiant_sensors/humidity", Utility.humidity, hostname="localhost")

    @staticmethod
    def cpu_temp():
        Utility.cputemp = CPUTemperature().temperature
        print("CPU temperature: %f °C" % Utility.cputemp)
        publish.single("/raspberry/cpu/temp", Utility.cputemp, hostname="localhost")

    @staticmethod
    def cpu_usage():
        Utility.usage = psutil.cpu_percent(interval=0, percpu=False)
        print("CPU usage: %f %%" % Utility.usage)
        publish.single("/raspberry/cpu/usage", Utility.usage, hostname="localhost")
