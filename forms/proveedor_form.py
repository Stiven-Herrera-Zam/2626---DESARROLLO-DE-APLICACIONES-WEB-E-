from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length, Email

class ProveedorForm(FlaskForm):
    ruc = StringField('RUC', validators=[
        DataRequired(message="El RUC es obligatorio."),
        Length(min=10, max=13, message="El RUC debe tener entre 10 y 13 dígitos.")
    ])
    empresa = StringField('Empresa Proveedora', validators=[
        DataRequired(message="La razón social o empresa es obligatoria.")
    ])
    contacto = StringField('Contacto Directo', validators=[
        DataRequired(message="El nombre de contacto es obligatorio.")
    ])
    telefono = StringField('Teléfono', validators=[
        DataRequired(message="El teléfono es obligatorio.")
    ])
    ciudad = StringField('Ciudad', validators=[
        DataRequired(message="La ciudad es obligatoria.")
    ])
    submit = SubmitField('Guardar Proveedor')