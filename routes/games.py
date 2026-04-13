from datetime import datetime, timezone
from flask import Blueprint, request, jsonify
from models import Game
from extensions import db

games_bp = Blueprint('games', __name__)

@games_bp.route('/games', methods=['POST'])
def create_game():
    data = request.get_json()

    print('data', data)

    title = data.get('title')
    description = data.get('description')
    genre = data.get('genre')
    rating = data.get('rating')
    game_url = data.get('game_url')
    created_at = db.Column(
        db.DateTime, 
        default=lambda: datetime.now(timezone.utc)
    )
    

    if not title or not description or not genre or not rating or not game_url:
        return jsonify({"error": "missing field"}), 400
    
    game = Game(
        title = title,
        description = description,
        genre = genre,
        rating = rating,
        game_url = game_url,
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
            "genre": game.genre,
            "rating": game.rating,
            "game_url": game.game_url,
            "created_at": game.created_at
        })

    return jsonify(all_games), 200

@games_bp.route('/games/<int:id>', methods=['PUT'])
def update_game(id):
    game = Game.query.get(id)

    if not game:
        return jsonify({"error": "game not found"}), 404
    
    data = request.get_json()

    game.title = data.get("title", game.title)
    game.description = data.get("description", game.description)
    game.genre = data.get("genre", game.genre)
    game.rating = data.get("rating", game.rating)
    game.game_url = data.get("game_url", game.game_url)

    db.session.commit()

    return jsonify({"message": "game updated"}), 200

@games_bp.route('/games/<int:id>', methods=['DELETE'])
def delete_game(id):
    game = Game.query.get(id)

    if not game:
        return jsonify({"error": "game not found"}), 404
    
    db.session.delete(game)
    db.session.commit()

    return jsonify({"messgae": "game deleted"}), 200

@games_bp.route('/games/<int:id>', methods=['GET'])
def get_game(id):
    game = Game.query.get(id)

    if not game:
        return jsonify({"error": "Game not found"}), 404

    return jsonify({
        "id": game.id,
        "title": game.title,
        "description": game.description,
        "genre": game.genre,
        "rating": game.rating,
        "game_url": game.game_url,
        "created_at": game.created_at
    }), 200

@games_bp.route('/games/search', methods=['GET'])
def search_games():
    query = request.args.get('q')

    if not query:
        return jsonify({"error": "query missing"}), 404
    
    games = Game.query.filter(Game.title.ilike(f"%{query}%")).all()

    searched_games = []
    for game in games:
        searched_games.append({
            "id": game.id,
            "title": game.title,
            "description": game.description,
            "genre": game.genre,
            "rating": game.rating,
            "game_url": game.game_url,
            "created_at": game.created_at
        })

    return jsonify(searched_games)

