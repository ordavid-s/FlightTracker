from flask import Flask, render_template, session, url_for, request, redirect, jsonify
from PacketParserInterface import PacketParserInterface
from callbacks import *

app = Flask(__name__)
app.secret_key = 'veryyy_secret'

bssid_data = {}
essid_data = {}
problem_data = {}
dvr_data = {}
flight_path = []
targets = []


def parse_gps(path):
    gps_data = []
    timestamps = []
    with open(path) as f:
        lines = [l.rstrip('\n').split(",") for l in f.readlines()]
    for l in lines:
        timestamps.append(int(l[0]))
        gps_data.append([float(l[2]), float(l[3])])
    return timestamps, gps_data

# with app.app_context():
#     # TODO : make sure time stamp data is sorted and gps data matches!
#     gps_data = parse_gps("./data.csv")
#     print("(+) Analyzing Data...")
#     file_path = "./resources/long.pcap"
#     path = "/home/ordavid/Desktop/PacketParser/mypipe"
#     pi = PacketParserInterface(file_path, path, parser_path="./PacketParser")
#     # relevant register callbacks
#     pi.read_data()
#     pi.clean()


bssid_data = {
    "a": [{"location": [51.508, -0.11], "rssi": -90, 'bssid': 'aa:bb:cc:dd:ee:ff', 'ssid': "cool"}],
    "b": [{"location": [51.512, -0.15], "rssi": -55, 'bssid': 'aa:bb:cc:dd:ee:ff', 'ssid': "nice"}]
        }

essid_data = {
    "Location 1": [{"location": [51.508, -0.11], "rssi": -90, 'bssid': 'aa:bb:cc:dd:ee:ff', 'ssid': "cool"}],
    "Location 2": [{"location": [51.512, -0.15], "rssi": -55, 'bssid': 'aa:bb:cc:dd:ee:ff', 'ssid': "nice"}]
        }

problem_data = [
    {"location": [51.508, -0.11], "rssi": -90, 'bssid': 'aa:bb:cc:dd:ee:ff', 'ssid': "p1"},
    {"location": [51.508, -0.09], "rssi": -90, 'bssid': 'aa:bb:cc:dd:ee:ff', 'ssid': "p2"}
]

dvr_data = [
    {"location": [51.508, -0.11], "rssi": -90, 'bssid': 'aa:bb:cc:dd:ee:ff', 'ssid': "p1"},
    {"location": [51.508, -0.09], "rssi": -90, 'bssid': 'aa:bb:cc:dd:ee:ff', 'ssid': "p2"}
]

flight_path = [
    [51.508, -0.08],
    [51.508, -0.10],
    [51.508, -0.11],
    [51.514, -0.13],
]

targets = [
    {"location": [51.508, -0.11], "rssi": -90, 'bssid': 'aa:bb:cc:dd:ee:ff', 'ssid': "p1"},
    {"location": [51.508, -0.09], "rssi": -90, 'bssid': 'aa:bb:cc:dd:ee:ff', 'ssid': "p2"}
]


@app.route('/')
def index():
    if 'selected_networks' not in session:
        session['selected_networks'] = []
    sidebar_width = 300
    ess_list = {"Location 1": ["a", "b"], "Location 2": ["c"]}

    # Render the template with the map
    return render_template('index.html',
                           ess_list=ess_list,
                           sidebar_width=sidebar_width)


@app.route('/update_networks', methods=['POST'])
def update_networks():
    response = {}
    for net, status in request.form.items():
        if net in bssid_data:
            response[net] = bssid_data[net]
        elif net in essid_data:
            response[net] = essid_data[net]
    return jsonify(response)


@app.route('/update_constants', methods=['POST'])
def update_constants():
    response = {}
    for const_name, status in request.form.items():
        if const_name == "flightPath":
            response[const_name] = flight_path
        if const_name == "problem":
            response[const_name] = problem_data
        if const_name == "dvr":
            response[const_name] = dvr_data
        if const_name == "targets":
            response[const_name] = targets
    return jsonify(response)


if __name__ == '__main__':
    app.run(debug=True)
