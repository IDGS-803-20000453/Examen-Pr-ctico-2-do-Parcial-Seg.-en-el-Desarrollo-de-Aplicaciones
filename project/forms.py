from wtforms import Form, StringField, IntegerField, validators

class ProductoForm(Form):
    nombre = StringField('Nombre del producto', validators=[validators.DataRequired()])
    precio = IntegerField('Precio', validators=[validators.DataRequired()])
    marca = StringField('Marca', validators=[validators.DataRequired()])
    cantidad = IntegerField('Cantidad', validators=[validators.DataRequired()])

