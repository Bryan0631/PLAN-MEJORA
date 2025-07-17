from App import db, bcrypt # Importa la instancia de db y bcrypt desde App/__init__.py
from flask_login import UserMixin 

class User(db.Model, UserMixin):
    __tablename__ = 'Usuarios' 

    id_usuario = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False) # Almacenará el hash de la contraseña
    rol = db.Column(db.Enum('admin', 'empleado'), default='empleado', nullable=False) # Rol del usuario
    fecha_creacion = db.Column(db.TIMESTAMP, default=db.func.current_timestamp())

   
    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8') # en esta linea se aplica la libreria bcrypt para encriptar la contraseña

 
    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password) # en esta linea se verifica la contraseña ingresada con el hash almacenado


    def get_id(self):
        return str(self.id_usuario)


    def __repr__(self):
        return f"<User('{self.username}', '{self.email}', '{self.rol}')>"

