from flask import request, Blueprint, jsonify
from ..common import database as db
from .models import UserEntity

users = Blueprint("users", __name__, url_prefix="/users")

@users.route("/create", methods=["POST"])
def create_post():
   if request.method == "POST":
      # Creating a user object
      user = UserEntity(
         name=request.form.get("name"),
         email=request.form.get("email"),
         password=request.form.get("password")
      )
      
      # Committing a new user to the database
      db.session.add(user)
      db.session.commit()
      
      # Return a success response
      return jsonify(status=201, success=True, user=user.to_dict())


@users.route("/get-all")
def fetch_all_posts():
   # Fetching all the user records and serializing it into json
   users = [user.to_dict() for user in UserEntity.query.all()]
   # Returning the list of users available in our database
   return jsonify(users)


@users.route("/<userId>")
def find_one_user(userId):
   # Fetching a single post with the post-id
   user = UserEntity.query.get(int(userId))
   
   # Checking if the post exists!
   if user is None:
      return jsonify(
         status=404,
         message="No user was found with the given post-id",
         reason="Resources Unavailable"
      )
   
   # Returning the post with the specific post-id
   return jsonify(status=200, user=user.to_dict())


@users.route("/<userId>", methods=["DELETE"])
def delete_post(userId):
   # Fetching a single post with the post-id to check whether post
   # exists before trying to delete it from the database
   user = UserEntity.query.get(int(userId))
   
   # If not post exists?
   if user is None:
      return jsonify(
         status=404,
         message="Cannot delete user with the given post-id",
         reason="Resources Unavailable"
      )
   
   # Deleting the post from the database
   db.session.delete(user)
   db.session.commit()
   
   # Sending back the success response
   return jsonify(status=200, message="User was removed!")


@users.route("/<userid>", methods=["PUT"])
def give_api(userid):
   # Fetching a single post with the post-id to check whether post
   # exists before trying to update to the database
   user = UserEntity.query.get(int(userid))
   
   # If user does not exists?
   if user is None:
      return jsonify(
         status=404,
         message="Cannot delete user with the given post-id",
         reason="Resources Unavailable"
      )
   
   # Updating user object
   for key, value in request.form.items():
      if key == "name":
         user.name = value
      elif key == "email":
         user.email = value
   
   # Committing the changes to the database
   db.session.commit()
   
   # Sending back the success response
   return jsonify(status=200, message="User updated!")