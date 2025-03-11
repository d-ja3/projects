
from flask import Flask
import socket

from flask import Flask, render_template, url_for

app = Flask(__name__)

@app.route("/")
def index():
    image_url = url_for('static', filename='SampleJPGImage_5mbmb.jpg')
    return render_template('index.html', image_url=image_url)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
