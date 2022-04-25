
from flask import Flask, render_template, Response,  request, session, redirect, url_for, send_from_directory, flash
from werkzeug.utils import secure_filename
from detect import *
import os
import torch
from importlib import import_module
# import camera driver
if os.environ.get('CAMERA'):
    Camera = import_module('camera_' + os.environ['CAMERA']).Camera
else:
    from yolov5_flask_distince import Camera
    #from camera import Camera
from flask_cors import *

app = Flask(__name__)
DETECTION_FOLDER = r'./static/detections'

# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER 
#app.config['DETECTION_FOLDER'] = DETECTION_FOLDER




@app.route('/')
def index():
    """Video streaming home page."""
    return render_template('index.html')

def gen(camera):
    """Video streaming generator function."""
    while True:
        frame = camera.get_frame()
        # a = camera.people_appeal()
        # print('a:{}0'.format(a))
        # for i in a:
        #     if i =='people':
        #         print('是people：{}}')
        #         people_appeal()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(Camera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')





if __name__ == "__main__":
    app.run(debug = True)
