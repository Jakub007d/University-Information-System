from flask import Flask
from config import Config
from datetime import timedelta
app = Flask(__name__)
app.config.from_object(Config)
app.permanent_session_lifetime = timedelta(hours=2)
app.debug = True
app.run()

from app import routes
