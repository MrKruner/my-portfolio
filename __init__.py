from flask import Flask, Blueprint


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY']='akandkl dasdDAddkln knmdklNDLKNdmaklnd'
    
    from .views import views
    
    app.register_blueprint(views, url_prefix='/')
    
    return app