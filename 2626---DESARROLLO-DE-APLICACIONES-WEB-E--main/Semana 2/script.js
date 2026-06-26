// Capturar el formulario por su id
const formProducto = document.getElementById("formProducto");

// Capturar los campos del formulario
const productoNombre = document.getElementById("productoNombre");
const productoDescripcion = document.getElementById("productoDescripcion");
const productoCategoria = document.getElementById("productoCategoria");

// Capturar elementos donde se mostrará información
const mensajeProducto = document.getElementById("mensajeProducto");
const listaProductos = document.getElementById("listaProductos");
const totalRegistros = document.getElementById("totalRegistros");

// Variable para contar los registros creados
let contadorRegistros = 0;

// Capturar el evento submit del formulario
formProducto.addEventListener("submit", function(evento) {

    // Evita que la página se recargue al enviar el formulario
    evento.preventDefault();

    // Obtener los valores escritos por el usuario
    const nombre = productoNombre.value.trim();
    const descripcion = productoDescripcion.value.trim();
    const categoria = productoCategoria.value.trim();

    // Validar que los campos no estén vacíos
    if (nombre === "" || descripcion === "" || categoria === "") {
        mensajeProducto.innerHTML = `
            <div class="alert alert-danger">
                Por favor, complete todos los campos.
            </div>
        `;
        return;
    }

    // Crear elementos HTML desde JavaScript usando createElement()
    const columna = document.createElement("div");
    const tarjeta = document.createElement("div");
    const cuerpoTarjeta = document.createElement("div");
    const tituloProducto = document.createElement("h5");
    const descripcionProducto = document.createElement("p");
    const categoriaProducto = document.createElement("span");
    const botonEliminar = document.createElement("button");

    // Asignar contenido a los elementos creados
    tituloProducto.textContent = nombre;
    descripcionProducto.textContent = descripcion;
    categoriaProducto.textContent = categoria;
    botonEliminar.textContent = "Eliminar";

    // Aplicar clases de Bootstrap a los elementos creados dinámicamente
    columna.classList.add("col-12", "col-md-6", "col-lg-4");
    tarjeta.classList.add("card", "h-100", "shadow", "border-0");
    cuerpoTarjeta.classList.add("card-body", "text-center");
    tituloProducto.classList.add("card-title", "text-primary");
    descripcionProducto.classList.add("card-text");
    categoriaProducto.classList.add("badge", "bg-success", "mb-3");
    botonEliminar.classList.add("btn", "btn-danger", "btn-sm", "mt-3");

    // Evento click para eliminar el registro
    botonEliminar.addEventListener("click", function() {
        columna.remove();

        contadorRegistros--;
        totalRegistros.textContent = contadorRegistros;

        mensajeProducto.innerHTML = `
            <div class="alert alert-warning">
                Producto eliminado correctamente.
            </div>
        `;
    });

    // Agregar elementos dentro de la tarjeta usando appendChild()
    cuerpoTarjeta.appendChild(tituloProducto);
    cuerpoTarjeta.appendChild(descripcionProducto);
    cuerpoTarjeta.appendChild(categoriaProducto);
    cuerpoTarjeta.appendChild(document.createElement("br"));
    cuerpoTarjeta.appendChild(botonEliminar);

    // Agregar el cuerpo dentro de la tarjeta
    tarjeta.appendChild(cuerpoTarjeta);

    // Agregar la tarjeta dentro de la columna
    columna.appendChild(tarjeta);

    // Agregar la columna completa a la página
    listaProductos.appendChild(columna);

    // Aumentar contador de registros
    contadorRegistros++;
    totalRegistros.textContent = contadorRegistros;

    // Mostrar mensaje de éxito
    mensajeProducto.innerHTML = `
        <div class="alert alert-success">
            Producto registrado correctamente.
        </div>
    `;

    // Limpiar formulario
    formProducto.reset();
});