from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
from sqlalchemy_serializer import SerializerMixin


db = SQLAlchemy()

class Episode(db.Model, SerializerMixin):
  __tablename__ = 'episodes'

  id = db.Column(db.Integer, primary_key=True)
  date = db.Column(db.String,nullable=False)
  number = db.Column(db.Integer, nullable=False)

  appearances = db.relationship('Appearance', back_populates='episode', cascade="all, delete-orphan")
  guests = db.relationship('Guest', secondary='appearances', back_populates='episodes')

  serialize_rules = ('-appearances.episode', '-appearances.guest.episodes', '-guests.episodes')

  def __repr__(self):
    return f"<Episode {self.date}>"

class Guest(db.Model, SerializerMixin):
  __tablename__ = 'guests'

  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String, nullable=False)
  occupation = db.Column(db.String, nullable=False)

  appearances = db.relationship('Appearance', back_populates='guest', cascade="all, delete-orphan") 
  episodes = db.relationship('Episode', secondary='appearances', back_populates='guests')

  serialize_rules = ('-appearances.guest', '-appearances.episode.guests', '-episodes.guests')

  def __repr__(self):
    return f"<Guest {self.name}>"
  
class Appearance(db.Model, SerializerMixin):
  __tablename__ = 'appearances'

  id = db.Column(db.Integer, primary_key=True)
  rating = db.Column(db.Integer, nullable=False)

  episode_id = db.Column(db.Integer, db.ForeignKey('episodes.id'), nullable=False)
  guest_id = db.Column(db.Integer, db.ForeignKey('guests.id'), nullable=False)

  episode = db.relationship('Episode', back_populates='appearances', overlaps="guests,episodes")
  guest = db.relationship('Guest', back_populates='appearances', overlaps="episodes,guests")

  serialize_rules = ('-episode.appearances', '-guest.appearances')

  @validates('rating')
  def validate_rating(self, key, value):
    if not (1 <= value <= 5):
            raise ValueError("Rating must be between 1 and 5.")
    return value 
  

  def __repr__(self):
    return f"<Appearance rating={self.rating}, episode={self.episode_id}, guest={self.guest_id}>"

