#!/usr/bin/env python3
"""A simple Flask app with user authentication features.
"""
from flask import Flask, jsonify, request
from auth import Auth


app = Flask(__name__)
AUTH = Auth()


@app.route("/", methods=["GET"])
def index():
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=["POST"])
def users():
    return jsonify({"message": "Bienvenue"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
