#!/usr/bin/python3

#required libraries
import sys                                 
import ssl
import json
import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(18, GPIO.OUT)

led_status = ""
led_type = ""
#called while client tries to establish connection with the server 
def on_connect(mqttc, obj, flags, rc):
    if rc==0:
        print ("Subscriber Connection status code: "+str(rc)+" | Connection status: successful")
        mqttc.subscribe("$aws/things/raspberry-pi/shadow/update/accepted", qos=0)
        #mqttc.publish("$aws/things/raspberry-pi/shadow/update",'{"state":{"reported":{"color":"Fu"}}}')#The names of these topics start with $aws/things/thingName/shadow."
    elif rc==1:
        print ("Subscriber Connection status code: "+str(rc)+" | Connection status: Connection refused")

#called when a topic is successfully subscribed to
def on_subscribe(mqttc, obj, mid, granted_qos):
    print("Subscribed: "+str(mid)+" "+str(granted_qos)+"data"+str(obj))

#called when a message is received by a topic
def on_message(mqttc, obj, msg):
    print("Received message from topic: "+msg.topic+" | QoS: "+str(msg.qos)+" | Data Received: "+str(msg.payload))
    message = json.loads(str(msg.payload.decode('utf-8')))
    led_status = message['state']['reported']['sensor']
    led_type = message['state']['reported']['type']
    if led_type == "mobile":
        toggle_led(led_status)

def toggle_led(toggle_state):
    led_state = GPIO.input(18)
    print(led_state)
    if led_state == False and toggle_state == "led on":
        GPIO.output(18, GPIO.HIGH)
        mqttc.publish("$aws/things/raspberry-pi/shadow/update",'{"state":{"reported":{"sensor":"led on", "type":"button"}}}')
    elif led_state == True and toggle_state == "led off":
        GPIO.output(18, GPIO.LOW)
        mqttc.publish("$aws/things/raspberry-pi/shadow/update",'{"state":{"reported":{"sensor":"led off", "type":"button"}}}')

#creating a client with client-id=mqtt-test
mqttc = mqtt.Client(client_id="mqtt_test")

mqttc.on_connect = on_connect
mqttc.on_subscribe = on_subscribe
mqttc.on_message = on_message

#Configure network encryption and authentication options. Enables SSL/TLS support.
#adding client-side certificates and enabling tlsv1.2 support as required by aws-iot service
mqttc.tls_set(ca_certs="/home/pi/assignment4/rootCA.pem.crt",
	      certfile="/home/pi/assignment4/218662640e-certificate.pem.crt",
	      keyfile="/home/pi/assignment4/218662640e-private.pem.key",
              tls_version=ssl.PROTOCOL_TLSv1_2, 
              ciphers=None)

#connecting to aws-account-specific-iot-endpoint
mqttc.connect("a6yj6fmeodfph.iot.us-west-2.amazonaws.com", port=8883) #AWS IoT service hostname and portno

mqttc.loop_start()

while True:
    input_state = GPIO.input(23)
    led_state = GPIO.input(18)
    if input_state == False:
        print('Button Pressed')
        if led_state == False:
            GPIO.output(18, GPIO.HIGH)
            mqttc.publish("$aws/things/raspberry-pi/shadow/update",'{"state":{"reported":{"sensor":"led on", "type":"button"}}}')
        else:
            GPIO.output(18, GPIO.LOW)
            mqttc.publish("$aws/things/raspberry-pi/shadow/update",'{"state":{"reported":{"sensor":"led off", "type":"button"}}}')
        time.sleep(0.2)

mqttc.loop_stop()
#automatically handles reconnecting
#mqttc.loop_forever()


