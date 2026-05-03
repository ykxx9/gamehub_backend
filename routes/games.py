from datetime import datetime, timezone
from flask import Blueprint, request, jsonify
from models import Game, SavedGame
from extensions import db

games_bp = Blueprint('games', __name__)


# ---------------------------------------------------------------------------
# Helper: serialise a Game row to a dict
# ---------------------------------------------------------------------------
def serialize_game(game):
    return {
        "id": game.id,
        "title": game.title,
        "description": game.description,
        "genre": game.genre or "",
        "rating": game.rating,
        "game_url": game.game_url,
        "status": game.status or "released",
        "tags": game.tags or "",
        "likes": game.likes or 0,
        "downloads": game.downloads or 0,
        "developer_name": game.developer_name or "Unknown",
        "images": game.images or "",
        "user_id": game.user_id or 0,
        "created_at": game.created_at.isoformat() if game.created_at else None,
    }


# ---------------------------------------------------------------------------
# POST /games  — create
# ---------------------------------------------------------------------------
@games_bp.route('/games', methods=['POST'])
def create_game():
    data = request.get_json(silent=True) or {}

    title = data.get('title', '').strip()
    description = data.get('description', '').strip()
    genre = data.get('genre', '').strip()
    rating = data.get('rating')
    game_url = data.get('game_url', '').strip()
    status = data.get('status', 'released')
    tags = data.get('tags', '')
    developer_name = data.get('developer_name', 'Unknown').strip()
    images = data.get('images', '')
    user_id = data.get('user_id', 0)

    # Required field check
    if not title or not description or not genre or not game_url or not developer_name:
        return jsonify({"success": False, "error": "Missing required fields"}), 400

    # rating validation
    if rating is not None and not isinstance(rating, (int, float)):
        try:
            rating = float(rating)
        except (ValueError, TypeError):
            return jsonify({"success": False, "error": "rating must be a number"}), 400

    # status validation
    if status not in ("beta", "released"):
        return jsonify({"success": False, "error": "status must be 'beta' or 'released'"}), 400

    game = Game(
        title=title,
        description=description,
        genre=genre,
        rating=float(rating) if rating is not None else None,
        game_url=game_url,
        status=status,
        tags=tags,
        developer_name=developer_name,
        images=images,
        user_id=int(user_id) if user_id else 0,
        likes=0,
        downloads=0,
        created_at=datetime.now(timezone.utc),
    )
    db.session.add(game)
    db.session.commit()

    return jsonify({"success": True, "data": serialize_game(game)}), 201


# ---------------------------------------------------------------------------
# GET /games  — list all
# ---------------------------------------------------------------------------
@games_bp.route('/games', methods=['GET'])
def get_games():
    games = Game.query.all()
    return jsonify({"success": True, "data": [serialize_game(g) for g in games]}), 200


# ---------------------------------------------------------------------------
# GET /games/search  — search by title, genre, description
# ---------------------------------------------------------------------------
@games_bp.route('/games/search', methods=['GET'])
def search_games():
    query = request.args.get('q', '').strip()
    if not query:
        return jsonify({"success": False, "error": "query parameter 'q' is required"}), 400

    pattern = f"%{query}%"
    games = Game.query.filter(
        Game.title.ilike(pattern) |
        Game.genre.ilike(pattern) |
        Game.description.ilike(pattern)
    ).all()

    return jsonify({"success": True, "data": [serialize_game(g) for g in games]}), 200


# ---------------------------------------------------------------------------
# GET /games/<id>  — single game
# ---------------------------------------------------------------------------
@games_bp.route('/games/<int:id>', methods=['GET'])
def get_game(id):
    game = Game.query.get(id)
    if not game:
        return jsonify({"success": False, "error": "Game not found"}), 404
    return jsonify({"success": True, "data": serialize_game(game)}), 200


# ---------------------------------------------------------------------------
# PUT /games/<id>  — update
# ---------------------------------------------------------------------------
@games_bp.route('/games/<int:id>', methods=['PUT'])
def update_game(id):
    game = Game.query.get(id)
    if not game:
        return jsonify({"success": False, "error": "Game not found"}), 404

    data = request.get_json(silent=True) or {}

    # Optional field updates
    if 'title' in data:
        game.title = data['title']
    if 'description' in data:
        game.description = data['description']
    if 'genre' in data:
        game.genre = data['genre']
    if 'rating' in data:
        rating = data['rating']
        if not isinstance(rating, (int, float)):
            try:
                rating = float(rating)
            except (ValueError, TypeError):
                return jsonify({"success": False, "error": "rating must be a number"}), 400
        game.rating = float(rating)
    if 'game_url' in data:
        game.game_url = data['game_url']
    if 'status' in data:
        if data['status'] not in ("beta", "released"):
            return jsonify({"success": False, "error": "status must be 'beta' or 'released'"}), 400
        game.status = data['status']
    if 'tags' in data:
        game.tags = data['tags']
    if 'developer_name' in data:
        game.developer_name = data['developer_name']
    if 'images' in data:
        game.images = data['images']

    db.session.commit()
    return jsonify({"success": True, "data": serialize_game(game)}), 200


# ---------------------------------------------------------------------------
# DELETE /games/<id>
# ---------------------------------------------------------------------------
@games_bp.route('/games/<int:id>', methods=['DELETE'])
def delete_game(id):
    game = Game.query.get(id)
    if not game:
        return jsonify({"success": False, "error": "Game not found"}), 404

    db.session.delete(game)
    db.session.commit()
    return jsonify({"success": True, "data": {"message": "Game deleted"}}), 200


# ---------------------------------------------------------------------------
# POST /games/<id>/like  — increment likes
# ---------------------------------------------------------------------------
@games_bp.route('/games/<int:id>/like', methods=['POST'])
def like_game(id):
    game = Game.query.get(id)
    if not game:
        return jsonify({"success": False, "error": "Game not found"}), 404

    game.likes = (game.likes or 0) + 1
    db.session.commit()
    return jsonify({"success": True, "data": {"likes": game.likes}}), 200


# ---------------------------------------------------------------------------
# GET /games/user/<user_id>  — games by owner
# ---------------------------------------------------------------------------
@games_bp.route('/games/user/<int:user_id>', methods=['GET'])
def get_user_games(user_id):
    games = Game.query.filter_by(user_id=user_id).all()
    return jsonify({"success": True, "data": [serialize_game(g) for g in games]}), 200

@games_bp.route('/games/save', methods=['POST'])
def save_game():
    data = request.get_json(silent=True) or {}
    username = data.get('username')
    game_id = data.get('game_id')
    
    if not username or not game_id:
        return jsonify({"success": False, "error": "Missing fields"}), 400
    
    exists = SavedGame.query.filter_by(username=username, game_id=game_id).first()
    if exists:
        return jsonify({"success": False, "error": "Already saved"}), 400
    
    saved = SavedGame(username=username, game_id=game_id)
    db.session.add(saved)
    db.session.commit()
    return jsonify({"success": True}), 201

@games_bp.route('/games/saved/<username>', methods=['GET'])
def get_saved(username):
    saved_entries = SavedGame.query.filter_by(username=username).all()
    game_ids = [s.game_id for s in saved_entries]
    games = Game.query.filter(Game.id.in_(game_ids)).all() if game_ids else []
    return jsonify({"success": True, "data": [serialize_game(g) for g in games]}), 200

@games_bp.route('/games/save/<int:game_id>/<username>', methods=['DELETE'])
def remove_saved(game_id, username):
    saved = SavedGame.query.filter_by(username=username, game_id=game_id).first()
    if not saved:
        return jsonify({"success": False, "error": "Not found"}), 404
    db.session.delete(saved)
    db.session.commit()
    return jsonify({"success": True}), 200
