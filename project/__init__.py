import os
from flask import Flask
from flask_security import Security,SQLAlchemySessionUserDatastore
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

#Importamos los modelos
from.models import User, Role
userDataStore = SQLAlchemySessionUserDatastore(db,User,Role)

def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = os.urandom(24)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Kirizu26@localhost:3306/flasksecurity'

    app.config['SECURITY_PASSWORD_HASH'] = 'pbkdf2_shash512'
    app.config['SECURITY_PASSWORD_SALT'] = 'thisissecretsalt'

    #db.init_app(app)

    #login_manager = LoginManager()
    #login_manager.login_view = 'auth.login'
    #login_manager.init_app(app)
#
    #from .models import User
#
    #@login_manager.user_loader
    #def load_user(user_id):
    #    return User.query.get(int(user_id))
#
    from.auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from.main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app