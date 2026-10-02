from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

# Módulo de Usuarios para Autenticación
class User(UserMixin, db.Model):
    __tablename__ = 'usuarios'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'


# Módulo de Categorías de Productos
class Categoria(db.Model):
    __tablename__ = 'categorias'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)

    productos = db.relationship('Producto', backref='categoria_rel', lazy=True)

    def __repr__(self):
        return f'<Categoria {self.nombre}>'


# Módulo de Productos
class Producto(db.Model):
    __tablename__ = 'productos'

    id = db.Column(db.Integer, primary_key=True)
    codigo = db.Column(db.String(20), unique=True, nullable=False)
    nombre = db.Column(db.String(100), nullable=False)
    precio = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, nullable=False, default=0)

    categoria_id = db.Column(db.Integer, db.ForeignKey('categorias.id'), nullable=False)

    proveedor_id = db.Column(db.Integer, db.ForeignKey('proveedores.id'), nullable=True)
    proveedor_rel = db.relationship('Proveedor', backref='productos', lazy=True)

    def __repr__(self):
        return f'<Producto {self.nombre}>'


# Módulo de Clientes
class Cliente(db.Model):
    __tablename__ = 'clientes'

    id = db.Column(db.Integer, primary_key=True)
    cedula = db.Column(db.String(20), unique=True, nullable=False)
    nombre = db.Column(db.String(100), nullable=False)
    telefono = db.Column(db.String(20))
    correo = db.Column(db.String(120))
    ciudad = db.Column(db.String(50))

    def __repr__(self):
        return f'<Cliente {self.nombre}>'


# Módulo de Proveedores
class Proveedor(db.Model):
    __tablename__ = 'proveedores'

    id = db.Column(db.Integer, primary_key=True)
    ruc = db.Column(db.String(20), unique=True, nullable=False)
    nombre = db.Column(db.String(100), nullable=False)
    telefono = db.Column(db.String(20))
    correo = db.Column(db.String(120))
    direccion = db.Column(db.String(150))

    @property
    def empresa(self):
        return self.nombre

    @property
    def contacto(self):
        return self.correo

    @property
    def ciudad(self):
        return self.direccion

    def __repr__(self):
        return f'<Proveedor {self.nombre}>'


# Módulo de Ventas (Único y actualizado con todos los campos)
class Venta(db.Model):
    __tablename__ = 'ventas'

    id = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.DateTime, default=db.func.current_timestamp())
    total = db.Column(db.Numeric(10, 2), nullable=False)
    estado = db.Column(db.String(50), default='Completada')

    cliente_id = db.Column(db.Integer, db.ForeignKey('clientes.id'), nullable=False)
    cliente = db.relationship('Cliente', backref='ventas', lazy=True)

    def __repr__(self):
        return f'<Venta {self.id} - Total: {self.total}>'