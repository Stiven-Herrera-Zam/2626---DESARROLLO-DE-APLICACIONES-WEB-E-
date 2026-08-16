// ===============================
// DATOS DEL PROYECTO (ARRAY DE OBJETOS)
// ===============================

const productos = [
    {
        nombre: "Buje en Caucho",
        descripcion: "Fabricación de bujes resistentes para vehículos.",
        categoria: "Cauchos"
    },
    {
        nombre: "Base de Motor",
        descripcion: "Reduce vibraciones y proporciona estabilidad.",
        categoria: "Repuestos"
    }
];

// ===============================
// CAPTURA DE ELEMENTOS
// ===============================

const formProducto = document.getElementById("formProducto");
const productoNombre = document.getElementById("productoNombre");
const productoDescripcion = document.getElementById("productoDescripcion");
const productoCategoria = document.getElementById("productoCategoria");

const errorNombre = document.getElementById("errorNombre");
const errorDescripcion = document.getElementById("errorDescripcion");
const errorCategoria = document.getElementById("errorCategoria");

const mensajeProducto = document.getElementById("mensajeProducto");
const listaProductos = document.getElementById("listaProductos");
const totalRegistros = document.getElementById("totalRegistros");

// ===============================
// VALIDACIONES
// ===============================

function validarNombre() {

    const valor = productoNombre.value.trim();

    if (valor === "") {
        errorNombre.innerHTML =
            "<small class='text-danger'>El nombre es obligatorio</small>";
        return false;
    }

    if (valor.length < 3) {
        errorNombre.innerHTML =
            "<small class='text-danger'>Mínimo 3 caracteres</small>";
        return false;
    }

    errorNombre.innerHTML = "";
    return true;
}

function validarDescripcion() {

    const valor = productoDescripcion.value.trim();

    if (valor === "") {
        errorDescripcion.innerHTML =
            "<small class='text-danger'>La descripción es obligatoria</small>";
        return false;
    }

    if (valor.length < 10) {
        errorDescripcion.innerHTML =
            "<small class='text-danger'>Ingrese una descripción más completa</small>";
        return false;
    }

    errorDescripcion.innerHTML = "";
    return true;
}

function validarCategoria() {

    if (productoCategoria.value === "") {
        errorCategoria.innerHTML =
            "<small class='text-danger'>Seleccione una categoría</small>";
        return false;
    }

    errorCategoria.innerHTML = "";
    return true;
}

// ===============================
// RENDERIZAR PRODUCTOS
// ===============================

function renderizarProductos() {

    listaProductos.innerHTML = "";

    // Estructura repetitiva solicitada
    productos.forEach((producto, index) => {

        listaProductos.innerHTML += `
            <div class="col-md-4">
                <div class="card shadow h-100">
                    <div class="card-body">

                        <h5 class="card-title text-primary">
                            ${producto.nombre}
                        </h5>

                        <p class="card-text">
                            ${producto.descripcion}
                        </p>

                        <span class="badge bg-success">
                            ${producto.categoria}
                        </span>

                        <div class="mt-3">
                            <button
                                class="btn btn-danger btn-sm"
                                onclick="eliminarProducto(${index})">
                                Eliminar
                            </button>
                        </div>

                    </div>
                </div>
            </div>
        `;
    });

    totalRegistros.textContent = productos.length;

    // Condición solicitada
    if (productos.length === 0) {
        listaProductos.innerHTML = `
            <div class="alert alert-warning text-center">
                No existen productos registrados.
            </div>
        `;
    }
}

// ===============================
// ELIMINAR PRODUCTO
// ===============================

function eliminarProducto(indice) {

    productos.splice(indice, 1);

    mensajeProducto.innerHTML = `
        <div class="alert alert-warning">
            Producto eliminado correctamente.
        </div>
    `;

    renderizarProductos();
}

// ===============================
// EVENTO SUBMIT
// ===============================
const spinner = document.getElementById("spinnerCarga");

formProducto.addEventListener("submit", function (e) {

    e.preventDefault();

    const nombreValido = validarNombre();
    const descripcionValida = validarDescripcion();
    const categoriaValida = validarCategoria();

    if (!nombreValido || !descripcionValida || !categoriaValida) {

        mensajeProducto.innerHTML = `
            <div class="alert alert-danger">
                Existen errores en el formulario.
            </div>
        `;

        return;
    }

    spinner.classList.remove("d-none");

setTimeout(function () {

    const nuevoProducto = {
        nombre: productoNombre.value.trim(),
        descripcion: productoDescripcion.value.trim(),
        categoria: productoCategoria.value
    };

    productos.push(nuevoProducto);

    spinner.classList.add("d-none");

    mensajeProducto.innerHTML = `
        <div class="alert alert-success">
            Producto registrado correctamente.
        </div>
    `;

    formProducto.reset();

    renderizarProductos();

}, 1500);
});

// ===============================
// INICIO
// ===============================

renderizarProductos();