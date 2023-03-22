#Importamos la clase Blueprint del módulo flask
from flask import Blueprint, flash, redirect, render_template, request, url_for
#Importamos login_required, current_user de flask_security
from flask_security import login_required, current_user, roles_accepted
#Importamos el decorador login_required de flask_security
from flask_security.decorators import roles_required

from project.forms import ProductoForm
#Importamos el objeto de la BD desde __init__.py
from . import db
from .models import Producto


main = Blueprint('main', __name__)

#Definimos la ruta a la página principal
@main.route('/')
def index():
    return render_template('index.html')

#Definimos la ruta a la página de perfil
@main.route('/profile')
@login_required
@roles_required('admin')
def profile():
    return render_template('profile.html', name=current_user.name)

@main.route('/agregar', methods=['GET', 'POST'])
@login_required
@roles_required('admin')
def agregar_producto():
    form = ProductoForm(request.form)
    if request.method == 'POST' and form.validate():
        producto = Producto(nombre=form.nombre.data, precio=form.precio.data,
                            marca=form.marca.data, cantidad=form.cantidad.data)
        db.session.add(producto)
        db.session.commit()
        return redirect(url_for('main.lista_productos'))

    return render_template('agregar_producto.html', form=form)

@main.route('/lista_productos')
@login_required
@roles_required('admin')
def lista_productos():
    productos = Producto.query.all()
    return render_template('lista_productos.html', productos=productos)


@main.route('/productos/<int:id>/eliminar', methods=['POST', 'DELETE'])
@login_required
@roles_required('admin')
def eliminar_producto(id):
    producto = Producto.query.get(id)
    if producto:
        db.session.delete(producto)
        db.session.commit()
        flash('Producto eliminado exitosamente', 'success')
    else:
        flash('Producto no encontrado', 'error')
    return redirect(url_for('main.lista_productos'))

@main.route('/editar/<int:id>', methods=['GET', 'POST'])
@login_required
@roles_required('admin')
def editar_producto(id):
    producto = Producto.query.get_or_404(id)
    form = ProductoForm(request.form, obj=producto)
    if request.method == 'POST' and form.validate():
        form.populate_obj(producto)
        db.session.commit()
        return redirect(url_for('main.lista_productos'))

    return render_template('editar_producto.html', form=form, producto=producto)


#Definimos la ruta a la página de productos
@main.route('/productos')
@login_required
@roles_required('user')
def productos():
    productos = Producto.query.all()
    return render_template('productos.html', name=current_user.name, productos=productos)


@main.route('/contacto')
def contacto():
    return render_template('contacto.html')
