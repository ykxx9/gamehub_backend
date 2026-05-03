import random
from flask import Blueprint, jsonify
from models import Game

rand_bp = Blueprint('rand_bp', __name__)

@rand_bp.route('/games/random', methods=['GET'])
def get_random():
    games = Game.query.all()
    if not games:
        return jsonify({"success": False, "error": "No games found"}), 404
    
    g = random.choice(games)
    return jsonify({
        "success": True,
        "data": {
            "id": g.id,
            "title": g.title,
            "genre": g.genre,
            "description": g.description,
            "rating": g.rating,
            "game_url": g.game_url
        }
    })
