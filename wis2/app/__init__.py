from flask import Flask
from config import Config
from datetime import timedelta
app = Flask(__name__)
app.config.from_object(Config)
app.permanent_session_lifetime = timedelta(hours=2)

from app import routes

if __name__=="__main__":
    app.run(debug=True,host="127.0.0.1", port=5000)