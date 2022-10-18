import numpy as np
import sqlite3
import random
import io
from flask import Flask, render_template, Response, request
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
#3759233
app = Flask(__name__)

def getData(type_ ):
    if type_ == 'mqtt':
        connection = sqlite3.connect('mqtt_3759233.db') 
        cursor = connection.cursor() 
        cursor.execute("select * from mqtt_3759233")
        mqtt_rows = cursor.fetchall()
        connection.close()
        return mqtt_rows
    if type_ == 'socket':
        connection = sqlite3.connect('websocket_3759233.db') 
        cursor = connection.cursor() 
        cursor.execute("select * from websocket_3759233")
        socket_rows = cursor.fetchall()
        connection.close()
        return socket_rows


@app.route('/')
def index():
    global numSamples
    numSamples = 10
    
    mqtt_rows = getData('mqtt' )
    socket_rows = getData('socket')

    return render_template("index.html", mqtt_rows = mqtt_rows, socket_rows = socket_rows) 


@app.route('/mqtt_temp.png')
def mqtttemp_png():
    fig = create_figure("mqtt" , 1)
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')

@app.route('/mqtt_hum.png')
def mqtthum_png():
    fig = create_figure("mqtt" , 2)
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')

@app.route('/mqtt_pres.png')
def mqttpres_png():
    fig = create_figure("mqtt" , 3)
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')

@app.route('/socket_temp.png')
def sockettemp_png():
    fig = create_figure("socket" , 1)
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')

@app.route('/socket_hum.png')
def sockethum_png():
    fig = create_figure("socket" , 2)
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')

@app.route('/socket_pres.png')
def socketpres_png():
    fig = create_figure("socket" , 3)
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')


def create_figure(db , type_):
    numSamples = 500
    allData = getData(db)
    allData = np.swapaxes(allData, 0, 1)
    dates = allData[0]
    temps = allData[type_].astype(float) # type 0 = date, 1 = temp , 2 = humidity, 3 = pressure
    fig = Figure()
    axis = fig.add_subplot(1, 1, 1)
    
    xs = dates
    ys = temps
    axis.plot(xs, ys)
    axis.set_xticks([])
    
    if type_ == 1:
        fig.suptitle(db + " Temperature")
        axis.set_ylabel("Temperature")
    if type_ == 2:
        axis.set_ylabel("Humidity")
        fig.suptitle(db + " Humidity")
    if type_ == 3:
        fig.suptitle(db + " Pressure")
        axis.set_ylabel("Pressure")
    axis.set_xlabel("Date-Time")
    return fig


if __name__ == '__main__':
    
    app.run(debug=True, port = 5000, host='0.0.0.0')
