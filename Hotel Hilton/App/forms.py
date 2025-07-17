from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, HiddenField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError, Optional
from App.models import User 

# Formulario para el registro de nuevos usuarios
class RegistrationForm(FlaskForm):
    username = StringField('Nombre de Usuario', validators=[DataRequired(), Length(min=2, max=80)])
    email = StringField('Email', validators=[DataRequired(), Length(max=120)]) 
    password = PasswordField('Contraseña', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirmar Contraseña', validators=[DataRequired(), EqualTo('password', message='Las contraseñas deben coincidir.')])
    submit = SubmitField('Registrarse')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Ese nombre de usuario ya está en uso. Por favor, elige uno diferente.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Ese email ya está registrado. Por favor, elige uno diferente.')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()]) 
    password = PasswordField('Contraseña', validators=[DataRequired()])
    remember_me = BooleanField('Recordarme')
    submit = SubmitField('Iniciar Sesión')

# Formulario para la gestión de usuarios (añadir/editar) por un administrador
class UserForm(FlaskForm):
    id_usuario = HiddenField() 
    
    username = StringField('Nombre de Usuario', validators=[DataRequired(), Length(min=2, max=80)])
    email = StringField('Email', validators=[DataRequired(), Length(max=120)])
  
    password = PasswordField('Contraseña', validators=[Optional(), Length(min=6)])
    confirm_password = PasswordField('Confirmar Contraseña', validators=[EqualTo('password', message='Las contraseñas deben coincidir.')])
    rol = SelectField('Rol', choices=[('admin', 'Administrador'), ('empleado', 'Empleado')], validators=[DataRequired()])
    submit = SubmitField('Guardar Usuario')


    def validate_username(self, username):
        if self.id_usuario.data: 
            user = User.query.filter(User.username == username.data, User.id_usuario != self.id_usuario.data).first()
        else: # Si estamos creando un nuevo usuario
            user = User.query.filter_by(username=username.data).first()
        
        if user:
            raise ValidationError('Ese nombre de usuario ya está en uso. Por favor, elige uno diferente.')

    def validate_email(self, email):
        # Similar a la validación de username
        if self.id_usuario.data:
            user = User.query.filter(User.email == email.data, User.id_usuario != self.id_usuario.data).first()
        else: 
            user = User.query.filter_by(email=email.data).first()
        
        if user:
            raise ValidationError('Ese email ya está registrado. Por favor, elige uno diferente.')