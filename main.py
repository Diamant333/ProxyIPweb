from flask import Flask
import requests

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/<ip_address>')
def print_ip_address(ip_address):
    ip_avail = 0
    http_get_address = 'http://{}'.format(ip_address)
    try:
        ip_avail = requests.get(http_get_address)
    except Exception as e:
        mod_status = 'NoStatus'
    else:
        mod_status = 'Ok'

    return [ip_address, mod_status]


if __name__ == '__main__':
    app.run(debug=True)
