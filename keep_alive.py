from flask import Flask
from threading import Thread

app = Flask(__name__)

@app.route('/')
def home():
    return "hello"

def run():
  app.run(
        host='0.0.0.0', #place private IP here
        port=80
    )

def keep_alive():
    t = Thread(target=run)
    t.start()
