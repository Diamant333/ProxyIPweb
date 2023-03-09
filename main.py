from flask import Flask, render_template, request
import requests
import os
import time
import json

app = Flask(__name__, template_folder="template")


@app.route('/')
def index():
    proxy_list = []
    with open('config.cfg', 'r') as f:
        lines = f.readlines()
        if lines:
            path_data = lines[0].strip()
            with open(path_data, 'r') as proxy:
                proxy_lines = proxy.readlines()
                for proxy_line in proxy_lines:
                    if 'proxy' in proxy_line:
                        start = proxy_line.find('-e') + 2
                        end = proxy_line.find('00\n', start)
                        proxy_list.append(proxy_line[start:end])

    def proxy_status(ip_address):
        result = os.system("ping -c 1 " + ip_address)
        if result == 0:
            status = True
        else:
            status = False
        return status

    return render_template('index.html', proxy_list=proxy_list, proxy_status=proxy_status)



@app.route('/setting/', methods=['post', 'get'])
def setting():

    with open('config.cfg', 'r') as f:
        lineas = f.readlines()
        if lineas:
            path_data = lineas[0].strip()
        else:
            path_data = 'введите путь'

    if request.method == 'POST':
        with open('config.cfg', 'r') as f1, open('config.cfg', 'w') as f2:
            lines = f1.readlines()
            if lines:
                lines[0] = request.form.get('path')
            else:
                f2.write(request.form.get('path'))
                path_data = request.form.get('path')

    return render_template('setting.html', path_data=path_data)


@app.route('/<ip_address>')
def print_ip_address(ip_address):
    result = os.system("ping /n 1 " + ip_address)
    stop = 0
    status = 'Ok'
    while result != 0:
        if stop > 3:
            status = 'No connect'
            break
        result = os.system("ping /n 1 " + ip_address)
        print('Ожидаем связи с модемом')
        time.sleep(10)
        stop += 1

    return render_template('index.html', ip_address=ip_address, status=status)


@app.route('/ipping')
def proxy_status():
    global st
    if request.method == 'GET':
        ip_address = request.args.get('ip_address')
        result = os.system("ping /n 1 " + ip_address)
        if result == 0:
            st = 'True'
        else:
            st = 'False'
    return str(st)

@app.route('/speed')
def get_speed():
    global st
    if request.method == 'GET':
        ip_address = request.args.get('ip_address')

        requests.get('http://{}/goform/goform_set_cmd_process?isTest=false&goformId=LOGIN&password=YWRtaW4='.format(ip_address))
        result = requests.get('http://{}/goform/goform_get_cmd_process?multi_data=1&sms_received_flag_flag=0&sts_received_flag_flag=0&cmd=realtime_tx_thrpt%2Crealtime_rx_thrpt'.format(ip_address))
        data = result.json()

    return data

@app.route('/renew')
def renew():
    if request.method == 'GET':
        ip_address = request.args.get('ip_address')
        auth_modem = 'http://{}/goform/goform_set_cmd_process?isTest=false&goformId=LOGIN&password=YWRtaW4='.format(ip_address)
        reboot_modem = 'http://{}/goform/goform_set_cmd_process?isTest=false&goformId=TURN_OFF_DEVICE'.format(ip_address)
        requests.get(auth_modem)
        requests.get(reboot_modem)
    return "Ok"

if __name__ == '__main__':
    app.run(host='10.42.0.11', debug=True)
