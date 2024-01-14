#!/usr/bin/python3
""" Script that starts a Flask web application """
from flask import Flask

app = Flask(__name__)
app.url_map.strict_slashes = False

@app.route("/")
def home():
    """Home route"""
    return "Hello HBNB!"

@app.route("/hbnb")
def hbnb():
    """hbnb route"""
    return "HBNB"

@app.route("/c/<text>")
def custom_text(text):
    """<text> dyanmic param"""
    text = text.replace('_', ' ')
    return f"C {text}"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
