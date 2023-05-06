from itertools import filterfalse
from flask import Flask, render_template, jsonify, request
import datetime
import threading
import os
import logging

app = Flask(__name__)
app.config["CACHE_TYPE"] = "null"
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

outputURLs = ["", "", "", "", ""]
PATH_PREFIX = "/home/piMD/MeArm/code/webserver/"
OUTPUT_PATH = PATH_PREFIX + "static/images/scan_output/"
textLog = ''

masterIP = None
server_thread = None
_start_callback = None
_stop_callback = None

######################### OUTPUTS #########################
# This is the main page
@app.route('/')
def index():
    global masterIP
    ip = request.remote_addr

    if (masterIP is None or ip == masterIP):
        now = datetime.datetime.now()
        timeStr = now.strftime("%Y-%m-%d %H:%M:%S") 
        templateData = { 'time': timeStr}

        masterIP = request.remote_addr
        return render_template('index.html', **templateData)
    else:
        return 'Server busy', 503

# Handles output images
@app.route("/get-images-links")
def update():
    images = []
    for i in range(0, 4):
        images.append(outputURLs[i])
    return jsonify(images)
    
def updateOutput(newURL):
    print("-------------------- WEBSERVER UPDATING  DATA --------------------")
    global outputURLs
    outputURLs.insert(0, newURL)
    if (len(outputURLs) >= 5):
        for i in range(4, len(outputURLs)):
            # delete the old files
            filepath = PATH_PREFIX + outputURLs[i]
            if (os.path.exists(filepath)):
                try:
                    os.remove(filepath)
                    print(f"{filepath} deleted successfully")
                except Exception as e:
                    print(f"Error deleting {filepath}: {e}")
            else: print(f"file at {filepath} doesn't exist")
            # update the list (trim and leave only the first 4)        
        outputURLs = outputURLs[:4]
    print('updating output. result: ' + str(outputURLs))
    print("Webserver updated")

# Handles output log
@app.route("/get-log")
def get_log():
    return jsonify(textLog)

def add_msg(msg):
    global textLog
    textLog += '<br>' + msg;

######################### INPUTS #########################
@app.route("/<action>")
def action(action):
    if (action == 'start'):
        print('Start clicked')
        startSystem()

    elif (action == 'stop'):
        print('Stop clicked')
        stopSystem()

    elif (action == 'clear_log'): clearLog()
    return '', 204
    #return render_template('index.html', **templateData)

def startSystem():
    _start_callback()
    return

def stopSystem():
    _stop_callback()
    return

def clearLog():
    global textLog
    textLog = ''
    return

def startServer(startCallback, stopCallback):
    global server_thread, _start_callback, _stop_callback
    _start_callback = startCallback
    _stop_callback = stopCallback

    server_thread = threading.Thread(name='server', target=lambda: app.run(app.run(port=80, host='0.0.0.0', use_reloader=False, debug=False))).start()

    

