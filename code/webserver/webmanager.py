from itertools import filterfalse
import random
from flask import Flask, render_template, jsonify, send_file, send_from_directory
import datetime
import threading

app = Flask(__name__)
app.config["CACHE_TYPE"] = "null"

outputURLs = ["", "", "", "", ""]

######################### OUTPUTS #########################
@app.route('/')
def index():
    now = datetime.datetime.now()
    timeStr = now.strftime("%Y-%m-%d %H:%M:%S") 
    outputPath = "/images/scan_output/"
    imgStr = "/images/scan_output/Sonar_result_at_2023-05-01_16_54_28.png"
    templateData = { 
        'time': timeStr,
        'sub1': imgStr
        }
    #return '', 204
    return render_template('index.html', **templateData)

@app.route("/update")
def update():
    #data = 'this is a string: ' + str(random.random())
    #return jsonify(data)
    #path = 'images/scan_output/sonar1.jpg'
    #return send_file(path, mimetype='image/png')
    images = []
    for i in range(0, 4):
        images.append(outputURLs[i])
    return jsonify(images)
    
def updateOutput(newURL):
    print('new url: ' + newURL)
    global outputURLs
    outputURLs.insert(0, newURL)
    if (len(outputURLs) >= 5):
        outputURLs = outputURLs[:4]
    print('updating output. result: ' + str(outputURLs))

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