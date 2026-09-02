from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length, Email, Optional

class ClienteForm(FlaskForm):
    cedula = StringField('Cédula / RUC', validators=[
        DataRequired(message="La cédula o RUC es obligatoria."),
        Length(min=10, max=13, message="Debe tener entre 10 y 13 dígitos.")
    ])
    nombre = StringField('Nombre / Razón Social', validators=[
        DataRequired(message="El nombre es obligatorio.")
    ])
    telefono = StringField('Teléfono', validators=[
        Optional(),
        Length(min=7, max=15, message="El teléfono debe tener entre 7 y 15 dígitos.")
    ])
    correo = StringField('Correo Electrónico', validators=[
        DataRequired(message="El correo es obligatorio."),
        Email(message="Ingrese un correo electrónico válido.")
    ])
    ciudad = StringField('Ciudad', validators=[
        DataRequired(message="La ciudad es obligatoria.")
    ])
    submit = SubmitField('Guardar Cliente')