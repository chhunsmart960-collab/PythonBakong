import requests
from flask import Flask, render_template, abort, request,redirect,url_for,flash,session
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
import config
from datetime import timedelta
from dotenv import load_dotenv
load_dotenv()


app = Flask(__name__)

app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "default-fallback-secret-key-for-testing")
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(hours=12)


app.config.from_object(config)

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
app.config['UPLOAD_FOLDER'] = os.path.join(BASE_DIR, 'static', 'uploads')
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(os.path.join(BASE_DIR, 'instance'), exist_ok=True)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(BASE_DIR, "instance", "app.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

import routes

@app.before_request
def before_request():
    url = request.path
    print("REQUEST PATH:", request.path)
    if url.startswith('/admin'):
        if not session.get("user_id"):
            flash("Please log in first.", "warning")
            return redirect(url_for("login", next=request.path))



if __name__ == "__main__":
    app.run()
