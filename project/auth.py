#Importamos los módulos a usar de flask
from flask import Blueprint, render_template, redirect, url_for, request, flash
#Importamos los módulos de seguridad para las funciones hash
from werkzeug.security import generate_password_hash, check_password_hash

#Importamos el método login_required de flask_security
from flask_security import login_required
#Importamos los métodos login_user, logout_user flask_security.utils
#########################################################################################
from flask_security.utils import login_user, logout_user, hash_password, encrypt_password
##########################################################################################
#Importamos el modelo del usuario
from . models import User
#Importamos el objeto de la BD y userDataStore desde __init__
from . import db, userDataStore

#Creamos el BluePrint y establecemos que todas estas rutas deben estar dentro de /security para sobre escribir las vistas por omisión de flask-security.
#Por lo que ahora las rutas deberán ser /security/login y security/register
auth = Blueprint('auth', __name__, url_prefix='/security')
from flask import current_app as app

@auth.route('/login')
def login():
    return render_template('/security/login.html')

@auth.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    #Consultamos si existe un usuario ya registrado con el email.
    user = User.query.filter_by(email=email).first()

    #Verificamos si el usuario existe
    #Tomamos el password proporcionado por el usuario lo hasheamos, y lo comparamos con el password de la base de datos.
    if user and check_password_hash(user.password, password):
        app.logger.info('Inicio de sesión exitoso para el usuario %s con contraseña %s y ID %s', email, password, user.id)


        if user.has_role('admin'):
            login_user(user, remember=remember)
            return redirect(url_for('main.profile'))
        elif user.has_role('user'):
            login_user(user, remember=remember)
            return redirect(url_for('main.productos'))
    else:
        app.logger.warning ('Inicio de sesión incorrecto verifique su correo %s y/o contraseña %s', email, password)

        flash('El usuario y/o la contraseña son incorrectos')
        return redirect(url_for('auth.login'))
    
    #Si llegamos a este punto sabemos que el usuario tiene datos correctos.
    #Creamos una sessión y logueamos al usuario
    login_user(user, remember=remember)
    return redirect(url_for('main.profile'))

# Reemplazamos signup por register
@auth.route('/register')
def register():
    return render_template('/security/register.html')

@auth.route('/register', methods=['POST'])
def register_post():
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')
     # Verificar si los campos no están en blanco
    if len(email) == 0 or len(name) == 0 or len(password) == 0:
        app.logger.error('Registro de cuenta incorrecto: se proporcionó un campo vacío')
        flash('Debe proporcionar un correo electrónico, nombre y contraseña para registrarse')
        return redirect(url_for('auth.register'))
    #Consultamos si existe un usuario ya registrado con el email.
    user = User.query.filter_by(email=email).first()

    if user: #Si se encontró un usuario, redireccionamos de regreso a la página de registro
        app.logger.warning ('Registro de cuenta incorrecto, el correo:  %s ya esta en uso', email)

        flash('El correo electrónico ya existe')
        return redirect(url_for('auth.register'))

    #Creamos un nuevo usuario con los datos del formulario.
    # Hacemos un hash a la contraseña para que no se guarde la versión de texto sin formato
    #new_user = User(email=email, name=name, password=generate_password_hash(password, method='sha256'))
    app.logger.info('Registro exitoso para el usuario %s con contraseña %s', email, password)

    userDataStore.create_user(

        name=name, email=email, password=generate_password_hash(password, method='sha256')

    )
    #userDataStore.create_user(
        #name=name, email=email, password=encrypt_password(password)
    #)
    
    #Añadimos el nuevo usuario a la base de datos.
    #db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('auth.login'))


@auth.route('/logout')
@login_required
def logout():
    #Cerramos la sessión
    logout_user()
    return redirect(url_for('main.index'))
