from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length

class ProveedorForm(FlaskForm):
    ruc = StringField('RUC', validators=[DataRequired(), Length(min=10, max=13)])
    empresa = StringField('Empresa Proveedora', validators=[DataRequired()])
    contacto = StringField('Contacto Directo', validators=[DataRequired()])
    telefono = StringField('Teléfono', validators=[DataRequired()])
    ciudad = StringField('Ciudad', validators=[DataRequired()])
    submit = SubmitField('Guardar Proveedor')