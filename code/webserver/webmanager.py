from itertools import filterfalse
import random
from flask import Flask, render_template, jsonify, send_file, send_from_directory
import datetime
import threading
import os

app = Flask(__name__)
app.config["CACHE_TYPE"] = "null"

outputURLs = ["", "", "", "", ""]
PATH_PREFIX = "/home/piMD/MeArm/code/webserver/"
OUTPUT_PATH = PATH_PREFIX + "static/images/scan_output/"

######################### OUTPUTS #########################
@app.route('/')
def index():
    now = datetime.datetime.now()
    timeStr = now.strftime("%Y-%m-%d %H:%M:%S") 
    templateData = { 'time': timeStr}

    ## clean up scan_output on startup
    #for filename in os.listdir(OUTPUT_PATH):
    #    file_path = os.path.join(OUTPUT_PATH, filename)
    #    try:
    #        if os.path.isfile(file_path):
    #            os.remove(file_path)
    #            print(f"{filename} deleted successfully")
    #    except Exception as e:
    #        print(f"Error deleting {file_path}: {e}")
    return render_template('index.html', **templateData)

@app.route("/update")
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
    print("-------------------- UPDATED --------------------")

@app.route("/update-forced")
def updatef():
    now = datetime.datetime.now()
    timeStr = now.strftime("%Y-%m-%d %H:%M:%S") 
    outputPath = "/images/scan_output/"
    imgStr = "/images/scan_output/Sonar_result_at_2023-05-01_16_54_28.png"
    templateData = { 
    'time': timeStr,
    'sub1': imgStr
    }
    return render_template('index.html', **templateData)

######################### INPUTS #########################
@app.route("/<action>")
def action(action):
    if (action == 'pause'):
        print('Pause clicked')
    elif (action == 'resume'):
        print('Resume clicked')
    elif (action == 'clear_log'):
        print('Clear log clicked')
        pass
    return '', 204
    #return render_template('index.html', **templateData)

def pauseSystem():
    return

def resumeSystem():
    return

def clearLog():
    return

######################### MAIN #########################
#if __name__ == '__main__':
#    app.run(debug=True, port=80, host='0.0.0.0')


def startServer():
    threading.Thread(target=lambda: app.run(app.run(port=80, host='0.0.0.0', use_reloader=False, debug=False))).start()
    #app.run(debug=True, port=80, host='0.0.0.0')

#def threadStartApp():
#    app.run(port=80, host='0.0.0.0', use_reloader=False, debug=False)