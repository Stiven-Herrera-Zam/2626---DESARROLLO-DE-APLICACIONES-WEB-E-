import os
import sqlite3
from flask import Flask, render_template, redirect, url_for, flash
from forms.cliente_form import ClienteForm
from forms.producto_form import ProductoForm
from forms.proveedor_form import ProveedorForm
from forms.facturacion_form import FacturacionForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'clave_secreta_cauchoscoca_2026'

# Configuración y conexión a la base de datos SQLite en data/
def get_db_connection():
    if not os.path.exists('data'):
        os.makedirs('data')
    conn = sqlite3.connect('data/cauchoscoca.db')
    conn.row_factory = sqlite3.Row  # Permite acceder a las columnas por nombre
    return conn

# Listas en memoria para los módulos aún no migrados a BD
lista_clientes = []
lista_proveedores = []
lista_facturas = []
lista_ventas = []

# Servicios de muestra para el index
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

@app.route('/productos', methods=['GET', 'POST'])
def productos():
    form = ProductoForm()
    
    # 1. Validación del formulario con WTForms
    if form.validate_on_submit():
        codigo = form.codigo.data
        nombre = form.nombre.data
        categoria = form.categoria.data
        precio = float(form.precio.data)
        stock = int(form.stock.data)

        conn = get_db_connection()
        try:
            # 2. Sentencia INSERT en la base de datos SQLite
            conn.execute(
                'INSERT INTO productos (codigo, nombre, categoria, precio, stock) VALUES (?, ?, ?, ?, ?)',
                (codigo, nombre, categoria, precio, stock)
            )
            conn.commit()
            flash('Producto guardado correctamente en la base de datos.', 'success')
        except sqlite3.IntegrityError:
            flash('El código del producto ya existe en la base de datos.', 'danger')
        finally:
            conn.close()

        return redirect(url_for('productos'))

    # 3. Sentencia SELECT para listar los productos almacenados
    conn = get_db_connection()
    lista_productos = conn.execute('SELECT * FROM productos').fetchall()
    conn.close()

    return render_template('productos.html', form=form, lista_productos=lista_productos)

@app.route('/clientes', methods=['GET', 'POST'])
def clientes():
    form = ClienteForm()
    if form.validate_on_submit():
        nuevo_cliente = {
            'cedula': form.cedula.data,
            'nombre': form.nombre.data,
            'telefono': form.telefono.data,
            'correo': form.correo.data,
            'ciudad': form.ciudad.data
        }
        lista_clientes.append(nuevo_cliente)
        flash('Cliente registrado exitosamente.', 'success')
        return redirect(url_for('clientes'))
    return render_template('clientes.html', form=form, lista_clientes=lista_clientes)

@app.route('/proveedores', methods=['GET', 'POST'])
def proveedores():
    form = ProveedorForm()
    if form.validate_on_submit():
        nuevo_prov = {
            'ruc': form.ruc.data,
            'empresa': form.empresa.data,
            'contacto': form.contacto.data,
            'telefono': form.telefono.data,
            'ciudad': form.ciudad.data
        }
        lista_proveedores.append(nuevo_prov)
        flash('Proveedor registrado exitosamente.', 'success')
        return redirect(url_for('proveedores'))
    return render_template('proveedores.html', form=form, lista_proveedores=lista_proveedores)

@app.route('/facturacion', methods=['GET', 'POST'])
def facturacion():
    form = FacturacionForm()
    
    # Cargar opciones desde SQLite para el selector de productos
    conn = get_db_connection()
    productos_bd = conn.execute('SELECT * FROM productos').fetchall()
    conn.close()

    if lista_clientes:
        form.cliente.choices = [(c['cedula'], f"{c['cedula']} - {c['nombre']}") for c in lista_clientes]
    else:
        form.cliente.choices = [('', 'Sin clientes registrados')]

    if productos_bd:
        form.producto.choices = [(p['codigo'], f"{p['nombre']} (${p['precio']:.2f})") for p in productos_bd]
    else:
        form.producto.choices = [('', 'Sin productos registrados')]

    if form.validate_on_submit():
        factura = {
            'cliente': form.cliente.data,
            'producto': form.producto.data,
            'cantidad': form.cantidad.data
        }
        lista_facturas.append(factura)
        
        # Registrar también en el historial de ventas
        venta = {
            'numero': f"V-{len(lista_ventas) + 1:04d}",
            'cliente': form.cliente.data,
            'fecha': '2026-09-02',
            'total': 0.0,
            'estado': 'Completada'
        }
        lista_ventas.append(venta)

        flash('Factura generada y venta registrada correctamente.', 'success')
        return redirect(url_for('facturacion'))
        
    return render_template('facturacion.html', form=form, lista_clientes=lista_clientes, lista_productos=productos_bd)

@app.route('/ventas')
def ventas():
    return render_template('ventas.html', lista_ventas=lista_ventas)

@app.route('/quienes-somos')
def quienes_somos():
    return render_template('quienes_somos.html')

@app.route('/contacto')
def contacto():
    return render_template('contacto.html')

@app.route('/registro')
def registro():
    return render_template('registro.html')

if __name__ == '__main__':
    app.run(debug=True)