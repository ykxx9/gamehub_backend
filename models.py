from extensions import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)


class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    genre = db.Column(db.String(50))
    rating = db.Column(db.Float)
    game_url = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime)
    status = db.Column(db.String(20), default="released")
    tags = db.Column(db.String(200))          # Comma-separated
    likes = db.Column(db.Integer, default=0)
    downloads = db.Column(db.Integer, default=0)
    developer_name = db.Column(db.String(100), default="Unknown")
    images = db.Column(db.Text, default="")   # Comma-separated image URLs (max 5)
    user_id = db.Column(db.Integer, default=0) # FK to User.id (lightweight, no constraint)

class SavedGame(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    game_id = db.Column(db.Integer, db.ForeignKey('game.id'), nullable=False)