import paho.mqtt.client as mqtt
import time
import json
import sqlite3
#3759233
################ if db does not exist create it ################
try:
    connection = sqlite3.connect('mqtt_3759233.db')
    sqlite_create_table_query = '''CREATE TABLE mqtt_3759233 (
                                date_time datetime NOT NULL,
                                temperature FLOAT NOT NULL,
                                humidity FLOAT NOT NULL,
                                pressure FLOAT NOT NULL );'''

    cursor = connection.cursor()
    print("Successfully Connected to SQLite")
    cursor.execute(sqlite_create_table_query)
    connection.commit()
    print("SQLite table created")

    cursor.close()

except sqlite3.Error as error:
    print(error)
finally:
    if connection:
        connection.close()
################ if db does not exist create it ################

def insertIntoTable(date_time, temperature, humidity, pressure):
    # write to db start
        try:  
            connection    = sqlite3.connect('mqtt_3759233.db')
            cursor              = connection.cursor()
            sqlite_insert_query = """INSERT INTO mqtt_3759233
                                (date_time, temperature, humidity, pressure) 
                                VALUES 
                                (?, ?, ?, ?)"""

            data_t = (date_time, temperature, humidity, pressure)
            count = cursor.execute(sqlite_insert_query, data_t)
            connection.commit()
            cursor.close()

        except sqlite3.Error as error:
            print("Failed to insert data into sqlite table:", error)
        finally:
            if connection:
                connection.close()
        # write to db end

################ recieve and write to sqlite db ################
'''
def on_message(client, userdata, message):
    compiled = str(message.payload.decode("utf-8"))
    print("Received message: ", compiled)
    compiled = eval(compiled)

    temperature = compiled['temperature']
    humidity    = compiled['humidity']
    pressure    = compiled['pressure']
    date_time   = compiled['date_time']

    insertIntoTable(date_time, temperature, humidity, pressure)
'''
def on_message(client, userdata, message):
    compiled = str(message.payload.decode("utf-8"))
    print(compiled)

mqttBroker = "broker.emqx.io" #"192.168.2.114" #mosquitto broker on a seperate raspberry pi
client = mqtt.Client("server")
client.connect(mqttBroker)

client.loop_start()
client.subscribe("test/flutter_location")
client.on_message = on_message
time.sleep(3000)
client.loop_stop()