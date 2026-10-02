import os
from flask import Flask, render_template, redirect, url_for, flash, request
from flask_login import LoginManager, login_user, logout_user, login_required, current_user

from models import db, User, Categoria, Producto, Venta, Cliente, Proveedor

from forms.cliente_form import ClienteForm
from forms.producto_form import ProductoForm
from forms.proveedor_form import ProveedorForm
from forms.facturacion_form import FacturacionForm
from forms.login_form import LoginForm
from forms.usuario_form import UsuarioForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'clave_secreta_cauchoscoca_2026'

# Configuración de conexión a PostgreSQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg://postgres:admin123@localhost:5432/cauchoscoca_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# Login Manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Por favor inicia sesión para acceder a esta página.'
login_manager.login_message_category = 'warning'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Inicialización automática de tablas relacionales e inserción de categorías base
with app.app_context():
    db.create_all()
    if Categoria.query.count() == 0:
        cat1 = Categoria(nombre='Bujes Automotrices')
        cat2 = Categoria(nombre='Bases de Motor')
        cat3 = Categoria(nombre='Alzas de Amortiguador')
        db.session.add_all([cat1, cat2, cat3])
        db.session.commit()

servicios = [
    {'titulo': 'Bujes Automotrices', 'descripcion': 'Fabricación de bujes de alta resistencia para suspensión.'},
    {'titulo': 'Bases de Motor', 'descripcion': 'Soportes de motor duraderos para reducción de vibraciones.'},
    {'titulo': 'Alzas de Amortiguador', 'descripcion': 'Alzas a medida para todo tipo de vehículo industrial y liviano.'}
]

@app.route('/')
def index():
    return render_template('index.html', servicios=servicios)

@app.route('/inicio')
def inicio():
    return redirect(url_for('index'))

# --- MÓDULO DE AUTENTICACIÓN ---

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))

    form = UsuarioForm()
    if form.validate_on_submit():
        user_exist = User.query.filter_by(username=form.username.data).first()
        if user_exist:
            flash('El nombre de usuario ya está registrado.', 'danger')
            return render_template('registro.html', form=form)

        nuevo_usuario = User(username=form.username.data, email=form.email.data)
        nuevo_usuario.set_password(form.password.data)

        db.session.add(nuevo_usuario)
        db.session.commit()
        flash('Usuario registrado exitosamente. Inicia sesión.', 'success')
        return redirect(url_for('login'))

    return render_template('registro.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash(f'¡Bienvenido, {user.username}!', 'success')
            next_page = request.args.get('next')
            return redirect(next_page or url_for('dashboard'))

        flash('Usuario o contraseña incorrectos.', 'danger')

    return render_template('login.html', form=form)

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Has cerrado sesión correctamente.', 'info')
    return redirect(url_for('login'))

# --- MÓDULO CLIENTES (CRUD COMPLETO) ---

@app.route('/clientes', methods=['GET', 'POST'])
@login_required
def clientes():
    form = ClienteForm()
    if form.validate_on_submit():
        nuevo_cliente = Cliente(
            cedula=form.cedula.data,
            nombre=form.nombre.data,
            telefono=form.telefono.data,
            correo=form.correo.data,
            ciudad=form.ciudad.data
        )
        try:
            db.session.add(nuevo_cliente)
            db.session.commit()
            flash('Cliente registrado correctamente.', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Error al registrar el cliente: {e}', 'danger')

        return redirect(url_for('clientes'))

    lista_clientes = Cliente.query.order_by(Cliente.id.desc()).all()
    return render_template('clientes.html', form=form, lista_clientes=lista_clientes, cliente_editar=None)

@app.route('/clientes/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar_cliente(id):
    cliente = Cliente.query.get_or_404(id)
    form = ClienteForm(obj=cliente)

    if form.validate_on_submit():
        try:
            cliente.cedula = form.cedula.data
            cliente.nombre = form.nombre.data
            cliente.telefono = form.telefono.data
            cliente.correo = form.correo.data
            cliente.ciudad = form.ciudad.data

            db.session.commit()
            flash('Cliente actualizado con éxito.', 'success')
            return redirect(url_for('clientes'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error al actualizar el cliente: {e}', 'danger')

    lista_clientes = Cliente.query.order_by(Cliente.id.desc()).all()
    return render_template('clientes.html', form=form, lista_clientes=lista_clientes, cliente_editar=cliente)

@app.route('/clientes/eliminar/<int:id>', methods=['POST'])
@login_required
def eliminar_cliente(id):
    cliente = Cliente.query.get_or_404(id)
    try:
        db.session.delete(cliente)
        db.session.commit()
        flash('Cliente eliminado correctamente.', 'info')
    except Exception as e:
        db.session.rollback()
        flash(f'Error al eliminar el cliente: {e}', 'danger')

    return redirect(url_for('clientes'))

# --- MÓDULO PROVEEDORES (CRUD COMPLETO) ---

@app.route('/proveedores', methods=['GET', 'POST'])
@login_required
def proveedores():
    form = ProveedorForm()
    if form.validate_on_submit():
        nuevo_proveedor = Proveedor(
            ruc=form.ruc.data,
            nombre=form.empresa.data,
            correo=form.contacto.data,
            telefono=form.telefono.data,
            direccion=form.ciudad.data
        )
        try:
            db.session.add(nuevo_proveedor)
            db.session.commit()
            flash('Proveedor registrado con éxito.', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Error al registrar proveedor: {e}', 'danger')

        return redirect(url_for('proveedores'))

    lista_proveedores = Proveedor.query.order_by(Proveedor.id.desc()).all()
    return render_template('proveedores.html', form=form, lista_proveedores=lista_proveedores, proveedor_editar=None)

@app.route('/proveedores/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar_proveedor(id):
    proveedor = Proveedor.query.get_or_404(id)
    form = ProveedorForm(obj=proveedor)

    if form.validate_on_submit():
        try:
            proveedor.ruc = form.ruc.data
            proveedor.nombre = form.empresa.data
            proveedor.correo = form.contacto.data
            proveedor.telefono = form.telefono.data
            proveedor.direccion = form.ciudad.data

            db.session.commit()
            flash('Proveedor actualizado con éxito.', 'success')
            return redirect(url_for('proveedores'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error al actualizar el proveedor: {e}', 'danger')

    lista_proveedores = Proveedor.query.order_by(Proveedor.id.desc()).all()
    return render_template('proveedores.html', form=form, lista_proveedores=lista_proveedores, proveedor_editar=proveedor)

@app.route('/proveedores/eliminar/<int:id>', methods=['POST'])
@login_required
def eliminar_proveedor(id):
    proveedor = Proveedor.query.get_or_404(id)
    try:
        db.session.delete(proveedor)
        db.session.commit()
        flash('Proveedor eliminado correctamente.', 'info')
    except Exception as e:
        db.session.rollback()
        flash(f'Error al eliminar el proveedor: {e}', 'danger')

    return redirect(url_for('proveedores'))

# --- MÓDULO FACTURACIÓN / VENTAS ---

@app.route('/facturacion', methods=['GET', 'POST'])
@app.route('/ventas', methods=['GET', 'POST'])
@login_required
def facturacion():
    form = FacturacionForm()
    form.cliente.choices = [(c.id, f"{c.nombre} - {c.cedula}") for c in Cliente.query.all()]
    form.producto.choices = [(p.id, f"{p.nombre} (${p.precio})") for p in Producto.query.all()]

    if form.validate_on_submit():
        try:
            producto_id = int(form.producto.data)
            cantidad_vendida = int(form.cantidad.data)
            cliente_id = int(form.cliente.data)

            producto = Producto.query.get_or_404(producto_id)

            if producto.stock < cantidad_vendida:
                flash(f'Stock insuficiente. Solo hay {producto.stock} unidades disponibles.', 'danger')
                return redirect(url_for('facturacion'))

            total_venta = producto.precio * cantidad_vendida
            producto.stock -= cantidad_vendida

            nueva_venta = Venta(
                cliente_id=cliente_id,
                total=total_venta,
                estado='Completada'
            )

            db.session.add(nueva_venta)
            db.session.commit()
            
            flash('¡Factura generada y venta registrada con éxito!', 'success')
            return redirect(url_for('facturacion'))

        except Exception as e:
            db.session.rollback()
            flash(f'Error al procesar la factura: {e}', 'danger')

    lista_ventas = Venta.query.order_by(Venta.id.desc()).all()
    return render_template('facturacion.html', form=form, lista_ventas=lista_ventas)

# --- MÓDULO PRODUCTOS ---

@app.route('/productos', methods=['GET', 'POST'])
@login_required
def productos():
    form = ProductoForm()
    form.categoria_id.choices = [(c.id, c.nombre) for c in Categoria.query.all()]
    form.proveedor_id.choices = [(p.id, p.nombre) for p in Proveedor.query.all()]
    
    if form.validate_on_submit():
        nuevo_producto = Producto(
            codigo=form.codigo.data,
            nombre=form.nombre.data,
            precio=float(form.precio.data),
            stock=int(form.stock.data),
            categoria_id=int(form.categoria_id.data),
            proveedor_id=int(form.proveedor_id.data),
        )
        try:
            db.session.add(nuevo_producto)
            db.session.commit()
            flash('Producto guardado correctamente en PostgreSQL.', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Error al guardar el producto: {e}', 'danger')

        return redirect(url_for('productos'))

    lista_productos = Producto.query.order_by(Producto.id.desc()).all()
    return render_template('productos.html', form=form, lista_productos=lista_productos, producto_editar=None)

@app.route('/productos/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar_producto(id):
    producto = Producto.query.get_or_404(id)
    form = ProductoForm(obj=producto)
    form.categoria_id.choices = [(c.id, c.nombre) for c in Categoria.query.all()]
    form.proveedor_id.choices = [(p.id, p.nombre) for p in Proveedor.query.all()]

    if form.validate_on_submit():
        try:
            producto.codigo = form.codigo.data
            producto.nombre = form.nombre.data
            producto.precio = float(form.precio.data)
            producto.stock = int(form.stock.data)
            producto.categoria_id = int(form.categoria_id.data)
            producto.proveedor_id = int(form.proveedor_id.data)

            db.session.commit()
            flash('Producto actualizado con éxito en PostgreSQL.', 'success')
            return redirect(url_for('productos'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error al actualizar el producto: {e}', 'danger')

    lista_productos = Producto.query.order_by(Producto.id.desc()).all()
    return render_template('productos.html', form=form, lista_productos=lista_productos, producto_editar=producto)

@app.route('/productos/eliminar/<int:id>', methods=['POST'])
@login_required
def eliminar_producto(id):
    producto = Producto.query.get_or_404(id)
    try:
        db.session.delete(producto)
        db.session.commit()
        flash('Producto eliminado correctamente de PostgreSQL.', 'info')
    except Exception as e:
        db.session.rollback()
        flash(f'Error al eliminar el producto: {e}', 'danger')

    return redirect(url_for('productos'))

# --- PÁGINAS PÚBLICAS ---

@app.route('/quienes-somos')
def quienes_somos():
    return render_template('quienes_somos.html')

@app.route('/contacto')
def contacto():
    return render_template('contacto.html')

if __name__ == '__main__':
    app.run(debug=True)