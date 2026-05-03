import os
from flask import Flask
from flask_cors import CORS
from extensions import db
from models import User, Game
from routes.auth import auth_bp
from routes.games import games_bp
from random_game import rand_bp

app = Flask(__name__)
CORS(app)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()

app.register_blueprint(auth_bp)
app.register_blueprint(games_bp)
app.register_blueprint(rand_bp)

@app.route('/')
def home():
    return {"success": True, "data": "Vyntrix API is running"}

if __name__ == "__main__":
    app.run(debug=True, port=6090)