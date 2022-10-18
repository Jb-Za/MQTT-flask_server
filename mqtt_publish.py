import paho.mqtt.client as mqtt
from random import randrange, uniform
import time
from sense_emu import SenseHat
from datetime import datetime
#3759233
mqttBroker = "192.168.2.114" # mosquitto broker on a seperate raspberry pi
client = mqtt.Client("Temperature_Pi")
client.connect(mqttBroker)

# topics = ["iot/temperature", "iot/humidity", "iot/pressure"]

sense = SenseHat()

while True: # continue to send data until the program is terminated
    temperature = sense.temp
    humidity = sense.humidity
    pressure = sense.pressure

    date_time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")  # stringyfying the date and time

    compiled = {'temperature': temperature, 'humidity': humidity, 'pressure': pressure , 'date_time': date_time }
    # putting it all into a neat dict object
    
    
    client.publish("compiled", str(compiled))   # sending the dict object as a string. 
    #i wanted to send it as a dict object but it was not working.
    #print("Just published " + str(randNumber) + " to Topic TEMPERATURE")
    time.sleep(0.2)