from flask import Blueprint, request, jsonify
from ..common import database as db
from .models import CommentEntity

comments = Blueprint('comments', __name__, url_prefix='/comments')

@comments.route('/add', methods=['POST'])
def add_a_comment():
   # Adding a new comment to a video
   comment = CommentEntity(text=request.form.get('comment'), postID=request.form.get('postid'))
   # Saving the comment mapped to the specific post-id
   # Pushing the comment to the database
   db.session.add(comment)
   db.session.commit()
   # Sending back a success response to the client
   return jsonify(status='success', data=comment.to_dict(), message='Your comment was posted on a post!'), 201


@comments.route('/<commentID>')
def remove_comment(commentID):
   # Finding the comment with the given commentID
   comment = CommentEntity.query.get(int(commentID))
   # Does comment exists?
   if comment is None:
      return jsonify(status='error', data=None, message='Cannot remove a comment which is not available!'), 503
   # Removing/Deleting the comment from the database
   db.session.delete(comment)
   db.session.commit()
   # Sending back success response
   return jsonify(status='success', data=comment.to_dict(), message='Comment deleted!'), 200