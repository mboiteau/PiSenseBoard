import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
from Utility import Utility


class Client:
    
    def start(self):
        self.mqttc.loop_forever()

    def connect(self):
        self.mqttc.connect("localhost", 1883, 60)

    def on_connect(self, mqttc, obj, flags, rc):
        print("Connected with result code "+str(rc))
        mqttc.subscribe("/raspberry/led/#")

    def on_message(self, client, userdata, msg):
        print(msg.topic+" "+str(msg.payload))
        if "/raspberry/led/" in msg.topic:
            Utility.led_func(msg.topic, msg.payload)

    def on_publish(self, mqttc, obj, mid):
        print("mid: " + str(mid))


    def on_subscribe(self, mqttc, obj, mid, granted_qos):
        print("Subscribed: " + str(mid) + " " + str(granted_qos))

    def __init__(self):
        self.mqttc = mqtt.Client()
        self.mqttc.on_message = self.on_message
        self.mqttc.on_connect = self.on_connect
        self.mqttc.on_publish = self.on_publish
        self.mqttc.on_subscribe = self.on_subscribe
