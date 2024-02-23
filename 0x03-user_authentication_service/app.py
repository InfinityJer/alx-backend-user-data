#!/usr/bin/env python3
"""Basic Flask app with user authentication features.
"""
from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/", methods=["GET"])
def welcome():
    """A simple GET route returning a welcome message."""
    return jsonify({"message": "Bienvenue"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
