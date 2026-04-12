from flask import Blueprint, request, jsonify
from models import Game
from extensions import db

games_bp = Blueprint('games', __name__)

@games_bp.route('/games', methods=['POST'])
def create_game():
    data = request.get_json()

    title = data.get('title')
    description = data.get('description')
    game_url = data.get('game_url')

    if not title or not description or not game_url:
        return jsonify({"error": "missing field"}), 400
    
    game = Game(
        title = title,
        description = description,
        game_url = game_url
    )

    db.session.add(game)
    db.session.commit()

    return jsonify({"message": "games added"}), 201

@games_bp.route('/games', methods=['GET'])
def get_games():
    games = Game.query.all()

    all_games = []

    for game in games:
        all_games.append({
            "id": game.id,
            "title": game.title,
            "description": game.description,
            "game_url": game.game_url
        })

    return jsonify(all_games), 200

@games_bp.route('/games/<int:id>', methods=['PUT'])
def update_game():
    game = Game.query.get(id)

    if not game:
        return jsonify({"error": "game not found"}), 404
    
    data = request.get_json()

    game.title = data.get("title", game.title)
    game.description = data.get("description", game.description)
    game.game_url = data.get("game_url", game.game_url)

    db.session.commit()

    return jsonify({"message": "game updated"}), 200

@games_bp.route('/games/<int:id>', methods=['DELETE'])
def delete_game():
    game = Game.query.get(id)

    if not game:
        return jsonify({"error": "game not found"}), 404
    
    db.session.delete(game)
    db.session.commit()

    return jsonify({"messgae": "game deleted"}), 200






