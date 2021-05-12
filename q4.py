from flask import Flask
import psycopg2 as pc2


app = Flask(__name__)


@app.route("/")
def hello():
    return "Hello, World!"
