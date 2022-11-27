import subprocess
import sys
from flask import Flask, request
import pandas as pd

# import cv2
import requests
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

import json

import numpy as np


@app.route("/", methods=["GET", "POST"])
def index():
    output = request.get_json()

    city = output['city']
    days = float(output['days'])
    budget = int(output['budget'])

    r = requests.get(
        "https://api.openweathermap.org/geo/1.0/direct?q=" + city + "&limit=1&appid=d2f0f5194fc7dbce96a2303575bea5c5")
    data = r.json()
    lat = float(data[0]["lat"])
    long = float(data[0]["lon"])

    # data, _ = subprocess.Popen([sys.executable, "current.py", str(latitude) + "," + str(longitude)],
    #                            stdout=subprocess.PIPE).communicate()
    # data = {"city": city,  "days": days+100}
    #
    # lati = {"lat" : lat,  "long": lon}

    #         lat = 30.3165
    #         long = 78.0322

    #         lat = latitude
    #         long = longitude
    budget_n = budget/days
    if budget_n in range(0,2000):
        bud=0
    elif budget_n in range(2001, 3000):
        bud = 1
    elif budget_n in range(3001, 4000):
        bud = 2
    elif budget_n in range(4001, 5000):
        bud = 3
    else:
        bud= 4

    r = requests.get("https://maps.googleapis.com/maps/api/place/nearbysearch/json?keyword=hotels&location=" + str(
        lat) + "%2C" + str(long) + "&radius=500&maxprice="+str(bud)+"&type=lodging&key=AIzaSyDxcBJYDXKP9cOK6F9LjAA3jbQYxMtfxwc")
    data = r.json()

    j = requests.get("https://maps.googleapis.com/maps/api/place/nearbysearch/json?&location=" + str(lat) + "%2C" + str(
        long) + "&radius=25000&type=point_of_interest&maxprice="+str(bud)+"&tkeyword=places&key=AIzaSyDxcBJYDXKP9cOK6F9LjAA3jbQYxMtfxwc")
    data2 = j.json()

    t = requests.get("https://maps.googleapis.com/maps/api/place/nearbysearch/json?keyword=hotels&location=" + str(
        lat) + "%2C" + str(
        long) + "&radius=500&type=hospital&keyword=hospitalnearme&maxprice="+str(bud)+"&tkey=AIzaSyDxcBJYDXKP9cOK6F9LjAA3jbQYxMtfxwc")
    data3 = t.json()

    # print(data)
    # jsonString = json.loads(data)
    s1 = json.dumps(data)
    jsonstring = json.loads(s1)

    s2 = json.dumps(data2)
    jsonstring2 = json.loads(s2)

    data_temp = data2["results"]
    data_length = len(data_temp) - 1
    new_data = []
    i = 0
    for entry in data_temp:
        if i == int(budget):
            pass
            i = + 1
        else:
            new_data.append(budget)
            i = + 1

    s3 = json.dumps(data3)
    jsonstring3 = json.loads(s3)

    block, _ = subprocess.Popen([sys.executable, "tiff.py", str(lat) + "," + str(long)],
                                stdout=subprocess.PIPE).communicate()
    j = json.loads(block)



    combined = {"hospital": jsonstring3, "hotel": jsonstring, "Places": jsonstring2, "Budget": budget}

    # print((jsonstring))
    # print(type(jsonstring2))
    #

    return combined


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=2000)
