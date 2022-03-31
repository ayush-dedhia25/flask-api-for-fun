from flask import Blueprint, request, jsonify
from ..common import database as db
from .models import PostEntity

posts = Blueprint("posts", __name__, url_prefix="/posts")

@posts.route("/create", methods=["POST"])
def create_post():
   if request.method == "POST":
      # Creating a user object
      post = PostEntity(
         title=request.form.get("title"),
         body=request.form.get("body"),
         user_id=request.form.get("user_id")
      )
      
      # Committing a new user to the database
      db.session.add(post)
      db.session.commit()
      
      # Return a success response
      return jsonify(status=201, success=True, post=post.to_dict())


@posts.route("/get-all")
def fetch_all_posts():
   # Fetching all the post records and serializing it into json
   posts = [post.to_dict() for post in PostEntity.query.all()]
   # Returning the list of posts
   return jsonify(posts)


@posts.route("/<postId>")
def find_one_post(postId):
   # Fetching a single post with the post-id
   post = PostEntity.query.get(int(postId))
   
   # Checking if the post exists!
   if post is None:
      return jsonify(
         status=404,
         message="No post was found with the given post-id",
         reason="Resources Unavailable"
      )
   
   # Returning the post with the specific post-id
   return jsonify(status=200, post=post.to_dict())


@posts.route("/<postId>", methods=["DELETE"])
def delete_post(postId):
   # Fetching a single post with the post-id to check whether post
   # exists before trying to delete it from the database
   post = PostEntity.query.get(int(postId))
   
   # If not post exists?
   if post is None:
      return jsonify(
         status=404,
         message="Cannot delete post with the given post-id",
         reason="Resources Unavailable"
      )
   
   # Deleting the post from the database
   db.session.delete(post)
   db.session.commit()
   
   # Sending back the success response
   return jsonify(status=200, message="Post was removed!")


@posts.route("/<postid>", methods=["PUT"])
def give_api(postid):
   post = PostEntity.query.get(int(postid))
   if post is None:
      return jsonify(
         status=404,
         message="Cannot delete post with the given post-id",
         reason="Resources Unavailable"
      )
   
   # Updating user object
   for key, value in request.form.items():
      if key == "title":
         post.title = value
      elif key == "body":
         post.body = value
   
   # Committing the changes to the database
   db.session.commit()
   
   # Sending back the success response
   return jsonify(status=200, message="Post updated!")