from flask import Flask
import time
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello world!'

@app.route('/time')
def current_time():
    current_time = time.localtime()
    return ("The current time is " + 
          time.strftime("%Y-%m-%d %H:%M:%S", current_time))

app.run(host='0.0.0.0',
        port=8080,
        debug=True)
