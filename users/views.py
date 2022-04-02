from flask import request, Blueprint, jsonify
from ..common import database as db
from .models import UserEntity

users = Blueprint('users', __name__, url_prefix='/users')

@users.route('/create', methods=['POST'])
def create_post():
   # Checking if the user already exists
   if UserEntity.query.filter_by(email=request.form.get('email')).first():
      return jsonify(status='error', data=None, message='Email already in use'), 409
   # Creating a user object
   user_to_create = UserEntity(name=request.form.get('name'), email=request.form.get('email'), password=request.form.get('password'))
   # Committing a new user to the database
   db.session.add(user_to_create)
   db.session.commit()
   # Return a success response
   return jsonify(status='success', data=user_to_create.to_dict(), message='User has been registered!'), 201


@users.route('/get-all')
def fetch_all_posts():
   # Fetching all the user records and serializing it into json
   users = [user.to_dict() for user in UserEntity.query.all()]
   return jsonify(status='success', data=users, message='Successful Request'), 200


@users.route('/<userId>')
def find_one_user(userId):
   # Fetching a single post with the post-id
   user = UserEntity.query.get(int(userId))
   # Checking if the post exists!
   if user is None:
      return jsonify(status='error', data=None, message='User not found!'), 404
   # Returning the post with the specific post-id
   return jsonify(status='success', data=user.to_dict(), message='Successful Request'), 200


@users.route('/<userId>', methods=['DELETE'])
def delete_post(userId):
   # Fetching a single post with the post-id to check whether post
   # exists before trying to delete it from the database
   user = UserEntity.query.get(int(userId))
   # If not post exists?
   if user is None:
      return jsonify(status='error', data=None, message='User not found to delete!'), 404
   # Deleting the post from the database
   db.session.delete(user)
   db.session.commit()
   # Sending back the success response
   return jsonify(status='success', data=user.to_dict(), message='User was deleted successfully!'), 200


@users.route('/<userid>', methods=['PUT'])
def give_api(userid):
   # Fetching a single post with the post-id to check whether post
   # exists before trying to update to the database
   user = UserEntity.query.get(int(userid))
   # If user does not exists?
   if user is None:
      return jsonify(status='error', data=None, message='User not found to update!'), 404
   # Updating user object
   for key, value in request.form.items():
      if key == 'name':
         user.name = value
      elif key == 'email':
         user.email = value
   # Committing the changes to the database
   db.session.commit()
   # Sending back the success response
   return jsonify(status='error', data=None, message='User updated successfully!'), 200