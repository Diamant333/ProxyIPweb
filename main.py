from flask import Flask
import requests
import os
import time

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/<ip_address>')
def print_ip_address(ip_address):
    result = os.system("ping -c 1 " + ip_address)
    stop = 0
    while result != 0:
        time.sleep(10)
        result = os.system("ping -c 1 " + ip_address)
        print('Ожидаем связи с модемом')
        stop += 1
        if stop > 3:
            break

    return ip_address


if __name__ == '__main__':
    app.run(debug=True)
