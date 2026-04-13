import os
from flask import Flask
from flask_cors import CORS
from models import User
from extensions import db
from routes.auth import auth_bp
from models import User, Game
from routes.games import games_bp

app = Flask(__name__)
CORS(app)

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,POST,PUT,DELETE,OPTIONS')
    return response

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

app.register_blueprint(auth_bp)

app.register_blueprint(games_bp)

@app.route('/')
def home():
    return "api is running"

if __name__ == "__main__":
    app.run(debug=True, port=6090)