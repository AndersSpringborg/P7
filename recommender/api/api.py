from flask import Flask, request, jsonify
import json
import db

app = Flask(__name__)

@app.route('/data', methods = ['GET'])
def read_recommendation():
    return "GET request"

@app.route('/data', methods = ['POST'])
def write_data():
    return "POST request"

if (__name__ == "__main__"):
    app.run()