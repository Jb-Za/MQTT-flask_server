# tcp-client.py
#3759233
from sense_emu import SenseHat
import json
import time
from datetime import datetime
from socket import *
serverName = "192.168.2.112"
serverPort = 12000

sense = SenseHat()

clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName,serverPort))

try:
    while True: # continue to send data until the program is terminated
        temperature = sense.temp
        humidity = sense.humidity
        pressure = sense.pressure
        
        date_time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")    # stringyfying the date and time

        compiled = {'temperature': temperature, 'humidity': humidity, 'pressure': pressure , 'date_time': date_time }   
        # putting it all into a neat dict object
        print(compiled)

        clientSocket.send(str(compiled).encode('utf-8'))   
        # sending the dict object as a string. i wanted to send it as a dict object but it was not working. jsons maybe?
        
        time.sleep(0.5) # wait half a second before sending the next data
except KeyboardInterrupt:
    pass
    
clientSocket.close()

