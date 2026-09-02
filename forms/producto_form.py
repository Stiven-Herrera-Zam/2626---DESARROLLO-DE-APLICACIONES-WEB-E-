from flask_wtf import FlaskForm
from wtforms import StringField, DecimalField, IntegerField, SubmitField
from wtforms.validators import DataRequired, Length, NumberRange

class ProductoForm(FlaskForm):
    codigo = StringField('Código', validators=[
        DataRequired(message="El código es obligatorio."),
        Length(min=3, max=10, message="El código debe tener entre 3 y 10 caracteres.")
    ])
    nombre = StringField('Nombre del Producto', validators=[
        DataRequired(message="El nombre es obligatorio."),
        Length(min=3, max=100, message="El nombre debe tener entre 3 y 100 caracteres.")
    ])
    categoria = StringField('Categoría', validators=[
        DataRequired(message="La categoría es obligatoria.")
    ])
    precio = DecimalField('Precio ($)', validators=[
        DataRequired(message="Ingrese un precio válido."),
        NumberRange(min=0.01, message="El precio debe ser mayor a 0.")
    ])
    stock = IntegerField('Stock', validators=[
        DataRequired(message="Ingrese la cantidad en stock."),
        NumberRange(min=0, message="El stock no puede ser negativo.")
    ])
    submit = SubmitField('Guardar Producto')