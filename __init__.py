from flask import Flask
from .common import database as db
from .users.views import users
from .posts.views import posts

def create_app():
   app = Flask(__name__)
   app.config["SECRET_KEY"] = "Android*My*Care"
   app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite3"
   app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
   
   # Database Configuration
   db.init_app(app)
   with app.app_context():
      db.create_all()
   
   # Registering Blueprints here
   app.register_blueprint(users)
   app.register_blueprint(posts)
   
   # Returning app's instance
   return app