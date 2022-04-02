from datetime import datetime
from sqlalchemy_serializer import SerializerMixin
from ..common import database as db

class CommentEntity(db.Model, SerializerMixin):
   # Defining tables name for the database
   __tablename__ = 'comments'
   
   # Comments table Serialization
   serialize_only = ('commentID', 'text', 'createdAt')
   serialize_rules = ()
   
   # Defining table fields
   commentID = db.Column(db.Integer, primary_key=True)
   text = db.Column(db.Text, nullable=False)
   postID = db.Column(db.Integer, db.ForeignKey('posts.postID'), nullable=False, index=True)
   createdAt = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
   updatedAt = db.Column(db.DateTime, onupdate=datetime.utcnow)
   
   # String representation for self
   def __repr__(self):
      return f'<Comment id={self.commentID}, title=\'{self.text[0:15]}...\'>'
