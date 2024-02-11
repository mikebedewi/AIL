from flask import Flask

def create_app():
    app = Flask(__name__, static_url_path='/static')

    app.config['SECRET_KEY'] = 'secretkey'

    from .auth import auth

    app.register_blueprint(auth, url_prefix='/')
    
    return app
