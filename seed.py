from app import app
from extensions import db
from models import Game

def run_seed():
    with app.app_context():
        db.session.query(Game).delete()
        
        data = [
            {"title": "genshin impact", "genre": "RPG", "rating": 4.8, "desc": "Explore a massive open world with elemental magic."},
            {"title": "minecraft", "genre": "Simulation", "rating": 4.9, "desc": "Build and survive in a blocky, procedurally generated world."},
            {"title": "pokemon legends arceus", "genre": "Adventure", "rating": 4.5, "desc": "Catch Pokemon in the ancient Hisui region."},
            {"title": "call of duty", "genre": "Shooter", "rating": 4.2, "desc": "Fast-paced military combat and multiplayer."},
            {"title": "gta v", "genre": "Action", "rating": 4.9, "desc": "Crime epic set in the sprawling city of Los Santos."},
            {"title": "palworld", "genre": "Simulation", "rating": 4.4, "desc": "Collect mysterious creatures and build bases."},
            {"title": "red dead redemption 2", "genre": "Action", "rating": 5.0, "desc": "An epic tale of life in the Wild West."},
            {"title": "hotwheels", "genre": "Racing", "rating": 4.1, "desc": "Fast toy car racing on gravity-defying tracks."},
            {"title": "forza horizon", "genre": "Racing", "rating": 4.7, "desc": "Open world driving and car culture festival."},
            {"title": "resident evil", "genre": "Action", "rating": 4.6, "desc": "Survive the horrors in a zombie-infested mansion."}
        ]

        for item in data:
            g = Game(
                title=item["title"],
                genre=item["genre"],
                description=item["desc"],
                rating=item["rating"],
                game_url="placeholder",
                images="placeholder",
                status="released"
            )
            db.session.add(g)
        
        db.session.commit()
        print("Seed complete.")

if __name__ == "__main__":
    run_seed()
