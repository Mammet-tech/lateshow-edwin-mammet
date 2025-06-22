from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_restful import Api, Resource
from sqlalchemy.exc import IntegrityError

from models import db
from models import Episode, Guest, Appearance  

app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db.init_app(app)
migrate = Migrate(app, db)
api = Api(app)

#Routes
class EpisodeList(Resource):
    def get(self):
        episodes = Episode.query.all()
        return [e.to_dict() for e in episodes], 200
    
class EpisodeByID(Resource):
    def get(self, id):
        ep = Episode.query.get(id)
        if ep:
            return ep.to_dict(), 200
        return {"error": "Episode not found"}, 404
    
class GuestList(Resource):
    def get(self):
        guests = Guest.query.all()
        return [g.to_dict() for g in guests], 200
    
class AppearanceCreate(Resource):
    def post(self):
        data = request.get_json()

        errors = []

        # Validate required fields
        required_fields = ['rating', 'episode_id', 'guest_id']
        for field in required_fields:
            if field not in data:
                errors.append(f"{field} is required.")

        # Validate rating range
        rating = data.get('rating')
        if isinstance(rating, int):
            if not (1 <= rating <= 5):
                errors.append("rating must be between 1 and 5.")
        else:
            errors.append("rating must be an integer.")

        # Validate foreign keys
        episode = Episode.query.get(data.get('episode_id'))
        guest = Guest.query.get(data.get('guest_id'))

        if not episode:
            errors.append("Episode not found.")
        if not guest:
            errors.append("Guest not found.")

        # Return errors if any
        if errors:
            return {"errors": errors}, 400

        # Create appearance
        try:
            appearance = Appearance(
                rating=rating,
                episode_id=episode.id,
                guest_id=guest.id
            )
            db.session.add(appearance)
            db.session.commit()

            # Prepare response
            response = {
                "id": appearance.id,
                "rating": appearance.rating,
                "guest_id": appearance.guest_id,
                "episode_id": appearance.episode_id,
                "episode": {
                    "id": episode.id,
                    "date": episode.date,
                    "number": episode.number
                },
                "guest": {
                    "id": guest.id,
                    "name": guest.name,
                    "occupation": guest.occupation
                }
            }

            return response, 201

        except Exception as e:
            db.session.rollback()
            return {"errors": [str(e)]}, 500
    
api.add_resource(EpisodeList, '/episodes')
api.add_resource(EpisodeByID, '/episodes/<int:id>')
api.add_resource(GuestList, '/guests')
api.add_resource(AppearanceCreate, '/appearances')


if __name__ == '__main__':
    app.run(port=5555, debug=True)
