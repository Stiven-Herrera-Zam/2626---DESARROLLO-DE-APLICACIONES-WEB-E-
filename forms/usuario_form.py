from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length

class UsuarioForm(FlaskForm):
    username = StringField('Usuario', validators=[
        DataRequired(message="El usuario es obligatorio."),
        Length(min=4, max=25, message="El usuario debe tener entre 4 y 25 caracteres.")
    ])
    email = StringField('Correo Electrónico', validators=[
        DataRequired(message="El correo es obligatorio."),
        Email(message="Ingrese un correo electrónico válido.")
    ])
    password = PasswordField('Contraseña', validators=[
        DataRequired(message="La contraseña es obligatoria."),
        Length(min=6, message="La contraseña debe tener al menos 6 caracteres.")
    ])
    submit = SubmitField('Registrarse')