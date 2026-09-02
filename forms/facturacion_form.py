from flask_wtf import FlaskForm
from wtforms import SelectField, IntegerField, SubmitField
from wtforms.validators import DataRequired, NumberRange

class FacturacionForm(FlaskForm):
    cliente = SelectField('Cliente', coerce=str, validators=[
        DataRequired(message="Seleccione un cliente.")
    ])
    producto = SelectField('Producto', coerce=str, validators=[
        DataRequired(message="Seleccione un producto.")
    ])
    cantidad = IntegerField('Cantidad', validators=[
        DataRequired(message="Ingrese la cantidad."),
        NumberRange(min=1, message="Debe facturar al menos 1 unidad.")
    ])
    submit = SubmitField('Generar Factura')