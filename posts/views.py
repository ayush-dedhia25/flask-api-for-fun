from flask import Blueprint, request, jsonify
from ..common import database as db
from .models import PostEntity

posts = Blueprint('posts', __name__, url_prefix='/posts')

@posts.route('/create', methods=['POST'])
def create_post():
   if request.method == 'POST':
      # Creating a user object
      post = PostEntity(title=request.form.get('title'), body=request.form.get('body'), user_id=request.form.get('user_id'))
      # Committing a new user to the database
      db.session.add(post)
      db.session.commit()
      # Return a success response
      return jsonify(status='success', data=post.to_dict(), message='User successfully registered!'), 200


@posts.route('/get-all')
def fetch_all_posts():
   # Fetching all the post records and serializing it into json
   posts = [post.to_dict() for post in PostEntity.query.all()]
   # Returning the list of posts
   return jsonify(status='success', data=posts, message=None), 200


@posts.route('/<postId>')
def find_one_post(postId):
   # Fetching a single post with the post-id
   post = PostEntity.query.get(int(postId))
   # Checking if the post exists!
   if post is None:
      return jsonify(status='error', data=None, message='Post not found!'), 404
   # Returning the post with the specific post-id
   return jsonify(status='success', data=post.to_dict(), message='successful Request'), 200


@posts.route('/<postId>', methods=['DELETE'])
def delete_post(postId):
   # Fetching a single post with the post-id to check whether post
   # exists before trying to delete it from the database
   post = PostEntity.query.get(int(postId))
   # If not post exists?
   if post is None:
      return jsonify(status='error', data=None, message='Unable to delete post with the given PostId'), 404
   # Deleting the post from the database
   db.session.delete(post)
   db.session.commit()
   # Sending back the success response
   return jsonify(status='success', data=None, message='Post deleted successfully!'), 200


@posts.route('/<postid>', methods=['PUT'])
def update_post(postid):
   # Checking if the post exists before trying to update it
   post = PostEntity.query.get(int(postid))
   # Does post exists?
   if post is None:
      return jsonify(status='error', data=None, message='No post found with the given PostId'), 404
   # Updating user object
   for key, value in request.form.items():
      if key == 'title':
         post.title = value
      elif key == 'body':
         post.body = value
   # Committing the changes to the database
   db.session.commit()
   # Sending back the success response
   return jsonify(status='success', data=post.to_dict(), message='Post Updated!'), 200