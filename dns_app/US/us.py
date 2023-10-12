from flask import Flask, request, abort
from socket import *
import json
import requests
app = Flask(__name__)

@app.route('/')
def Welcome_US():
    return 'Welcom to this User Server!'

@app.route('/fibonacci', methods = ['GET'])
def fibonacci():
    getrequest = request.args
    hostname = getrequest.get('hostname', None)
    fs_port = getrequest.get('fs_port', None)
    number = getrequest.get('number', None)
    as_ip = getrequest.get('as_ip', None)
    as_port = getrequest.get('as_port', None)

    if hostname == None or fs_port == None or number == None or as_ip == None or as_port == None:
        abort(400)
    
    socket_us = socket(AF_INET, SOCK_DGRAM)
    message = {
        'type':'A', 
        'name': hostname
    }
    message = json.dumps(message)
    socket_us.sendto(message.encode(), (as_ip, int(as_port)))
    msg, address = socket_us.recvfrom(2048)
    msg = msg.decode()
    print(msg)
    address_total = 'http://' + msg + ':' + fs_port + 'fabonacci?number=' + number
    print(address_total)
    response = requests.get(address_total)
    return response.text, 200
    
app.run(host = '0.0.0.0', port = 8080, debug = True)