from flask import Flask, render_template
import datetime

app = Flask(__name__)

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
if __name__ == '__main__':
    app.run(debug=True, port=80, host='0.0.0.0')