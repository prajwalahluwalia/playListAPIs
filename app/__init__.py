from flask import Flask
from .playlist import PlayList

playlist = PlayList()
app = Flask(__name__)

from app import routes

if __name__=="__main__":
    app.run(debug=True)