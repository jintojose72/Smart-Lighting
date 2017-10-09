#!/usr/bin/python3

#required libraries
import sys                                 
import ssl
import json
import paho.mqtt.client as mqtt
import time

led_state = ""
#led_type = ""
#called while client tries to establish connection with the server 
def on_connect(mqttc, obj, flags, rc):
    if rc==0:
        print ("Subscriber Connection status code: "+str(rc)+" | Connection status: successful")
        mqttc.subscribe("$aws/things/raspberry-pi/shadow/update/accepted", qos=0)
        mqttc.subscribe("$aws/things/raspberry-pi/shadow/get/accepted", qos=0)
    elif rc==1:
        print ("Subscriber Connection status code: "+str(rc)+" | Connection status: Connection refused")

#called when a topic is successfully subscribed to
def on_subscribe(mqttc, obj, mid, granted_qos):
    print("Subscribed: "+str(mid)+" "+str(granted_qos)+" data:"+str(obj))
    mqttc.publish("$aws/things/raspberry-pi/shadow/get", payload=None)

#called when a message is received by a topic
def on_message(mqttc, obj, msg):
    #print("Received message from topic: "+msg.topic+" | QoS: "+str(msg.qos)+" | Data Received: "+str(msg.payload))
    message = json.loads(str(msg.payload.decode('utf-8')))
    global led_state
    if led_state != str(message['state']['reported']['sensor']):
        led_state = str(message['state']['reported']['sensor'])
        if led_state == "led off":
            print("Led off. Enter on to switch on:")
        elif led_state == "led on":
            print("Led on. Enter off to switch off:")
    #led_type = message['state']['reported']['type']

#creating a client with client-id=mqtt-test
mqttc = mqtt.Client(client_id="mqtt_mobile")

mqttc.on_connect = on_connect
mqttc.on_subscribe = on_subscribe
mqttc.on_message = on_message

#Configure network encryption and authentication options. Enables SSL/TLS support.
#adding client-side certificates and enabling tlsv1.2 support as required by aws-iot service
mqttc.tls_set(ca_certs="/home/manoj/MS_Ebooks/IOT/Assignment4/rootCA.pem.crt",
	      certfile="/home/manoj/MS_Ebooks/IOT/Assignment4/218662640e-certificate.pem.crt",
	      keyfile="/home/manoj/MS_Ebooks/IOT/Assignment4/218662640e-private.pem.key",
              tls_version=ssl.PROTOCOL_TLSv1_2, 
              ciphers=None)

#connecting to aws-account-specific-iot-endpoint
mqttc.connect("a6yj6fmeodfph.iot.us-west-2.amazonaws.com", port=8883) #AWS IoT service hostname and portno

mqttc.loop_start()
while True:
    time.sleep(2)
    cmd = input()
    if cmd == "on":
        mqttc.publish("$aws/things/raspberry-pi/shadow/update",'{"state":{"reported":{"sensor":"led on", "type":"mobile"}}}')
    elif cmd == "off":
        mqttc.publish("$aws/things/raspberry-pi/shadow/update",'{"state":{"reported":{"sensor":"led off", "type":"mobile"}}}')

mqttc.loop_end()
#automatically handles reconnecting
#mqttc.loop_forever()
