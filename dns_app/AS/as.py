from socket import *
import json

#dns_database = {}
as_port = 53533
socket_as = socket(AF_INET, SOCK_DGRAM)
socket_as.bind(('', as_port))

while True:
    msg, address = socket_as.recvfrom(2048)
    msg = json.loads(msg.decode())

    # Registration request from fs
    if len(msg) == 4:
        type = msg['type']
        hostname = msg['name']
        ip = msg['value']
        ttl = msg['ttl']
        dns = {'type': type, 'name': hostname, 'value': ip, 'ttl': ttl}
        
        key = type + ' ' + hostname
        f = open('dns_database.json', 'w')
        f.write(json.dumps({key: dns}))
        f.close
        
        response = 'Registration succeeds!'
        response = json.dumps(response)
        socket_as.sendto(response.encode(), address)

    # DNS request from us
    elif len(msg) == 2:
        hostname = msg['name']
        type = msg['type']
        key = type + ' ' + hostname
        response = 'DNS Not Found.'
        
        f = open('dns_database.json', 'r')
        dns_database = json.load(f)
        f.close

        response = dns_database.get(key, response)
        response = json.dumps(response)
        socket_as.sendto(response.encode(), address)
