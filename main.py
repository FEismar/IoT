import network
import utime
from umqtt_simple import MQTTClient
import CCS811
from machine import Pin, ADC, I2C
import onewire, ds18x20, utime

wlanSSID = '********'
wlanPW = '********'
network.country('DE')

mqttBroker = 'mqtt.eclipseprojects.io' 
mqttClient = ''
mqttUser = 'mqtt-user'
mqttPW = '***********'

#Initialisierung Onboard LED
led_onboard = Pin('LED', Pin.OUT)
sensor_temp = ADC(4)

#Initialisierung Temp. Sensor
ds_pin = machine.Pin(16)
ds_sensor = ds18x20.DS18X20(onewire.OneWire(ds_pin))

#Scannen auf Geräte im OneWire-Bus
roms = ds_sensor.scan()
#print('Found DS devices: ', roms)

def wlanConnect(): 
    wlan = network.WLAN(network.STA_IF)
    if not wlan.isconnected():
        #print('WLAN-Verbindung herstellen:', wlanSSID)
        wlan.active(True)
        wlan.config(pm = 0xa11140) #Disable powersave mode
        wlan.connect(wlanSSID, wlanPW)
        for i in range(10):
            if wlan.status() < 0 or wlan.status() >= 3:
                break
            print('.')
            utime.sleep(1)
    if wlan.isconnected():
        print('WLAN-Verbindung hergestellt / WLAN-Status:', wlan.status())
    else:
        print('Keine WLAN-Verbindung / WLAN-Status:', wlan.status())
    return wlan

def mqttConnect():
    #print("MQTT-Verbindung herstellen: %s mit %s als %s" % (mqttClient, mqttBroker, mqttUser))
    client = MQTTClient(mqttClient, mqttBroker, port=1883,keepalive=60)
    client.set_last_will('ef/office/pico', str(-1))
    client.connect()
    return client

wlan = wlanConnect()
client = mqttConnect()

def mqttPublish(topic, data):
    client.publish(topic, data)
    #print(topic, data)
    return client

#main Methode
while True:
    if wlan.isconnected():
        i2c = I2C(0, scl=Pin(5), sda=Pin(4))
        utime.sleep(1)
        sensor_co2 = CCS811.CCS811(i2c=i2c, addr=90)
        utime.sleep(1)
        while True:
            if sensor_co2.data_ready():
                led_onboard.toggle()
                ds_sensor.convert_temp()
                rom = roms[0]
                
                #Daten lesen
                t = ds_sensor.read_temp(rom)
                co2 = sensor_co2.eCO2
                voc = sensor_co2.tVOC
                sensor_co2.put_envdata(humidity = 50, temp=t)
                print (co2, voc, t)
                
                #Daten veröffentlichen
                try:
                    mqttPublish('ef/office/eCO2', str(co2))
                except OSError:
                    print('Fehler: Keine MQTT-Verbindung CO2')
                utime.sleep(1)
            
                try:
                    mqttPublish('ef/office/tVOC', str(voc))
                except OSError:
                    print('Fehler: Keine MQTT-Verbindung VOC')
                utime.sleep(1)
            
                try:
                    mqttPublish('ef/office/temp', str(t))
                except OSError:
                    print('Fehler: Keine MQTT-Verbindung Temp')    
                led_onboard.toggle()
                utime.sleep(10)
            else:
                utime.sleep(10)
    else:
        wlanConnect()
        mqttConnect()

            
