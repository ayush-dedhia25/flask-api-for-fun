from flask import Flask
from flask_migrate import Migrate
from .common import database as db

# View Handlers
from .users.views import users
from .posts.views import posts
from .comments.views import comments

def create_app():
   app = Flask(__name__)
   app.config['SECRET_KEY'] = b'Android*My*Care'
   app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
   app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
   
   # Database migrations
   migrate = Migrate(app, db)
   
   # Database Configuration
   db.init_app(app)
   with app.app_context():
      db.create_all()
   
   # Registering Blueprints here
   app.register_blueprint(users)
   app.register_blueprint(posts)
   app.register_blueprint(comments)
   
   # Returning app's instance
   return app