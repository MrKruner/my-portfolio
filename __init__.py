from flask import Flask, Blueprint
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_socketio import SocketIO

db=SQLAlchemy()
migrate = Migrate()
socketio = SocketIO()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY']='akandkl dasdDAddkln knmdklNDLKNdmaklnd'
    app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///database.db'
    db.init_app(app)
    migrate.init_app(app)
    socketio.init_app(app)
    
    from .views import views
    
    app.register_blueprint(views, url_prefix='/')
    
    from .models import User
    login_manager = LoginManager()
    login_manager.login_view='views.login'
    login_manager.init_app(app)
    @login_manager.user_loader
    def load_user(id):
        # Load user from database, etc.
        return User.query.get(int(id))
    
    
    with app.app_context():
        db.create_all()
    
    return app

