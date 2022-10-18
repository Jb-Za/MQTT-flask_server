from socket import *
import sqlite3
from datetime import datetime
import json
#3759233
serverPort = 12000
serverSocket = socket(AF_INET,SOCK_STREAM)

serverSocket.bind(("192.168.2.112",serverPort))

################ if db does not exist create it ################
try:
    connection = sqlite3.connect('websocket_3759233.db')
    sqlite_create_table_query = '''CREATE TABLE websocket_3759233 (
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
            connection    = sqlite3.connect('websocket_3759233.db')
            cursor              = connection.cursor()
            sqlite_insert_query = """INSERT INTO websocket_3759233
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
serverSocket.listen(1)
print ("The server is ready to receive")
connectionSocket, addr = serverSocket.accept()
while True:
    try: 
        data = connectionSocket.recv(1024).decode()
        print(data)
        
        compiled = eval(data)

        temperature = compiled['temperature']
        humidity    = compiled['humidity']
        pressure    = compiled['pressure']
        date_time   = compiled['date_time']
        
        insertIntoTable(date_time, temperature, humidity, pressure)

        continue
    except Exception as ex:
        print (str(ex))
        connectionSocket.close()
        break
################ recieve and write to sqlite db ################

