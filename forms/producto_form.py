from flask_wtf import FlaskForm
from wtforms import StringField, DecimalField, IntegerField, SelectField, SubmitField
from wtforms.validators import DataRequired

class ProductoForm(FlaskForm):
    codigo = StringField('Código', validators=[DataRequired()])
    nombre = StringField('Nombre del Producto', validators=[DataRequired()])
    precio = DecimalField('Precio ($)', validators=[DataRequired()])
    stock = IntegerField('Stock', validators=[DataRequired()])
    categoria_id = SelectField('Categoría', coerce=int, validators=[DataRequired()])
    proveedor_id = SelectField('Proveedor', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Guardar Producto')