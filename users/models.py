from datetime import datetime
from sqlalchemy_serializer import SerializerMixin
from ..common import database as db
from ..posts.models import PostEntity

class UserEntity(db.Model, SerializerMixin):
   # Defining table name for the database
   __tablename__ = 'users'
   
   # Users table Serializating
   serialize_only = ('userID', 'name', 'email', 'createdAt', 'posts')
   serialize_rules = ()
   
   # Defining table fields
   userID = db.Column(db.Integer, primary_key=True)
   name = db.Column(db.String(20), nullable=False)
   email = db.Column(db.String(80), nullable=False, unique=True)
   password = db.Column(db.String(128), nullable=False)
   createdAt = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
   updatedAt = db.Column(db.DateTime, onupdate=datetime.utcnow)
   posts = db.relationship(PostEntity, backref='user', lazy='dynamic')
   
   # String representation for self
   def __repr__(self):
      return f'<User id={self.userID}, name=\'{self.name}\'>'

