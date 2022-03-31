from datetime import datetime
from sqlalchemy_serializer import SerializerMixin
from ..common import database as db

class PostEntity(db.Model, SerializerMixin):
   # Defining table name for the database
   __tablename__ = "posts"
   
   # User Serializating
   serialize_only = ("postID", "title", "body", "createdAt")
   serialize_rules = ()
   
   # Defining table fields
   postID = db.Column(db.Integer, primary_key=True)
   title = db.Column(db.String(50), nullable=False)
   body = db.Column(db.String(80), nullable=False)
   user_id = db.Column(db.Integer, db.ForeignKey("users.userID"), nullable=False, index=True)
   createdAt = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
   updatedAt = db.Column(db.DateTime, onupdate=datetime.utcnow)
   
   # String representation for self
   def __repr__(self):
      return f"<Post id={self.postID}, title='{self.title[0:15]}...'>"
