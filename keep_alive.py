from flask import Flask
from threading import Thread

app = Flask(__name__)

@app.route('/')
def home():
    return "hello"

def run():
  app.run(
        host='192.168.1.11', #place private IP here
        port=5000
    )

def keep_alive():
    t = Thread(target=run)
    t.start()
