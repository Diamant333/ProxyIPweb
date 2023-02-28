from flask import Flask, render_template, request
import requests
import os
import time

app = Flask(__name__, template_folder="template")


@app.route('/')
def index():

    return render_template('index.html')


@app.route('/setting/', methods=['post', 'get'])
def setting():

    with open('config.cfg', 'r') as f:
        if f.readlines():
            lineas = f.readlines()
            print(lineas)
            path_data = lineas[0].strip()
    if request.method == 'POST':
        with open('config.cfg', 'r') as f1, open('config.cfg', 'w') as f2:
            lines = f1.readlines()

            for line in lines:
                line = line.strip()
                if line == path_data:
                    f2.write(request.form.get('path'))
                else:
                    f2.write(request.form.get('path'))

    return render_template('setting.html')

@app.route('/<ip_address>')
def print_ip_address(ip_address):
    result = os.system("ping -c 1 " + ip_address)
    stop = 0
    status = 'Ok'
    while result != 0:
        if stop > 3:
            status = 'No connect'
            break
        result = os.system("ping -c 1 " + ip_address)
        print('Ожидаем связи с модемом')
        time.sleep(10)
        stop += 1

    return render_template('index.html', ip_address=ip_address, status=status)


if __name__ == '__main__':
    app.run(debug=True)
