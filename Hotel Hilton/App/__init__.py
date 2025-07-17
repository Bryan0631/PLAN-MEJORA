import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from dotenv import load_dotenv

# Cargar variables desde el archivo .env
load_dotenv()

# Inicialización de extensiones
db = SQLAlchemy()
csrf = CSRFProtect()
bcrypt = Bcrypt()
login_manager = LoginManager() 

def create_app():
    app = Flask(__name__)
    app.config.from_object('App.config.Config') 

    db.init_app(app) 
    csrf.init_app(app) 
    bcrypt.init_app(app) 
    login_manager.init_app(app) 
    login_manager.login_view = 'main.login' 
    login_manager.login_message_category = 'info' 

    from App.models import User

  
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))


    from App.routes import main as main_blueprint
    app.register_blueprint(main_blueprint)

 
    with app.app_context():
        db.create_all()

    return app

