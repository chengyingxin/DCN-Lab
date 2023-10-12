from flask import Flask, request, abort
from socket import *
import json
import requests
app = Flask(__name__)

def cal_fabonacci(n):
    if n < 0: abort(400)
    if n < 2: return n
    prev, curr = 0, 1
    for i in range(2, n + 1):
        fib = prev + curr
        prev, curr = curr, fib
    return curr

@app.route('/')
def Welcome_FS():
    return 'Welcom to this Fabonacci Server!'

@app.route('/register', methods = ['PUT'])
def FibonacciServer():
    getrequest = request.args
    hostname = getrequest.get('hostname', None)
    ip = getrequest.get('ip', None)
    as_ip = getrequest.get('as_ip', None)
    as_port = getrequest.get('as_port', None)

    if hostname == None  == None or ip == None or as_ip == None or as_port == None:
        abort(400)
    
    body = {
        "hostname": hostname,
        "ip": ip, 
        "as_ip": as_ip,
        "as_port": as_port
    }
    
    socket_fs = socket(AF_INET, SOCK_DGRAM)
    msg = {
            "type": "A",
            "name": hostname,
            "value": ip,
            "ttl": 10
    }
    msg = json.dumps(msg)
    socket_fs.sendto(msg.encode(), (as_ip, int(as_port)))
    confirm, _ = socket_fs.recvfrom(2048)
    socket_fs.close()
    return confirm.encode()



@app.route('/fibonacci', methods = ['GET'])
def fibonacci():
    getrequest = request.args
    number = getrequest.get('number', None)
    if not number.isnumeric:
        return 400
    return str(cal_fabonacci(int(number))), 200
    

app.run(host = '0.0.0.0', port = 9090, debug = True)