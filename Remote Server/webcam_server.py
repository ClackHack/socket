#Import necessary libraries
from flask import Flask, render_template, Response, request
import cv2, socket
import requests, threading
#Initialize the Flask app
running=False


sb = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sb.connect(("8.8.8.8", 80))
ip = str(sb.getsockname()[0])
sb.close()



class Webcam:
    def __init__(self, start=False):
        self.app=None
        self.running=False
        self.reload()
        if start:
            t = threading.Thread(target = self.start_server)
            t.start()
            
    def reload(self):
        app = Flask(__name__)
        
        @app.route('/')
        def index():
            return render_template('index.html')

        @app.route('/video_feed')
        def video_feed():
            '''if not self.running:
                return ""'''
            return Response(self.gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

        @app.route('/shutdown')
        def shutdown():
            global running
            shutdown_func = request.environ.get('werkzeug.server.shutdown')
            if shutdown_func is None:
                print("Shustdown failed")
            shutdown_func()
            running = False
            return "Shutting Down"
        self.app = app
    def start(self):
        self.running=True
        self.camera = cv2.VideoCapture(0)
        #self.app.run(host=ip, threaded=True,port=5000)
    def stop(self):
        self.running=False
        self.camera.release()
       #requests.get('http://'+ip+":5000/shutdown")
       #self.reload()
    def start_server(self):
        self.camera = cv2.VideoCapture(0)
        self.app.run(host=ip, threaded=True,port=5050)
    def gen_frames(self):
        if not self.running:
            return "https://i.kym-cdn.com/photos/images/original/001/293/685/010.jpg"  
        while True:
            if not self.running:
                yield ("https://i.kym-cdn.com/photos/images/original/001/293/685/010.jpg")
            success, frame = self.camera.read()  # read the camera frame
            if not success:
                break
            else:
                ret, buffer = cv2.imencode('.jpg', frame)
                frame = buffer.tobytes()
                yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
    
                


'''def start():
    app.run(host=ip,port=5000)

def stop():
    requests.get('http://'+ip+":5000/shutdown")'''

if __name__ == "__main__":
    #app.run(host=ip, debug=True)
    import time,_thread
    w = Webcam()
    time.sleep(8)
    print("start ")
    w.start()
    time.sleep(15)
    print("Killing")
    w.stop()
    #kthread.terminate()
    time.sleep(10)
    print('rebooting')
    w.start()

