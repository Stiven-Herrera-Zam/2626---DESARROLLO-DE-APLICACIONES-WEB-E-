from flask import Flask, render_template

app = Flask(__name__)

# Ruta Principal (Inicio)
@app.route('/')
@app.route('/home')
def home():
    return render_template('index.html', titulo="Inicio - Cauchos Coca")

# Rutas de los Módulos del Sistema
@app.route('/productos')
def productos():
    return render_template('productos.html', titulo="Productos")

@app.route('/clientes')
def clientes():
    return render_template('clientes.html', titulo="Clientes")

@app.route('/proveedores')
def proveedores():
    return render_template('proveedores.html', titulo="Proveedores")

@app.route('/facturacion')
def facturacion():
    return render_template('facturacion.html', titulo="Facturación")

@app.route('/ventas')
def ventas():
    return render_template('ventas.html', titulo="Ventas")

@app.route('/quienes-somos')
def quienes_somos():
    return render_template('quienes_somos.html', titulo="Quiénes Somos")

@app.route('/contacto')
def contacto():
    return render_template('contacto.html', titulo="Contacto")

@app.route('/registro')
def registro():
    return render_template('registro.html', titulo="Registro")

# Ejecución del servidor de desarrollo
if __name__ == '__main__':
    app.run(debug=True)