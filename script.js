    // Capturar el formulario por su id
    const formProducto = document.getElementById("formProducto");

    // Capturar los campos del formulario
    const productoNombre = document.getElementById("productoNombre");
    const productoDescripcion = document.getElementById("productoDescripcion");
    const productoCategoria = document.getElementById("productoCategoria");

    // Mensajes dinámicos de error o éxito
    const errorNombre = document.getElementById("errorNombre");
    const errorDescripcion = document.getElementById("errorDescripcion");
    const errorCategoria = document.getElementById("errorCategoria");

    // Capturar elementos donde se mostrará información
    const mensajeProducto = document.getElementById("mensajeProducto");
    const listaProductos = document.getElementById("listaProductos");
    const totalRegistros = document.getElementById("totalRegistros");

    // Variable para contar los registros creados
    let contadorRegistros = 0;

    // Función que valida el campo nombre del producto.
    function validarNombre() {

    const valor = productoNombre.value.trim();

    if (valor === "") {

        productoNombre.classList.add("is-invalid");
        productoNombre.classList.remove("is-valid");

        errorNombre.innerHTML =
            "<small class='text-danger'>El nombre es obligatorio</small>";

        return false;
    }

    // Comprueba que no esté vacío y que tenga al menos 3 caracteres.
    if (valor.length < 3) {

        productoNombre.classList.add("is-invalid");
        productoNombre.classList.remove("is-valid");

        errorNombre.innerHTML =
            "<small class='text-danger'>Mínimo 3 caracteres</small>";

        return false;
    }

    // Muestra mensajes dinámicos y aplica estilos Bootstrap de error o éxito.
        productoNombre.classList.remove("is-invalid");
        productoNombre.classList.add("is-valid");

        errorNombre.innerHTML = "";

        return true;
    }

    // Función que valida la descripción del producto.
    function validarDescripcion() {

    const valor = productoDescripcion.value.trim();

    if (valor === "") {

        productoDescripcion.classList.add("is-invalid");
        productoDescripcion.classList.remove("is-valid");

        errorDescripcion.innerHTML =
            "<small class='text-danger'>La descripción es obligatoria</small>";

        return false;
    }

    // // Verifica que el nombre tenga al menos 3 caracteres.
    if (valor.length < 10) {

        productoDescripcion.classList.add("is-invalid");
        productoDescripcion.classList.remove("is-valid");

        errorDescripcion.innerHTML =
            "<small class='text-danger'>Ingrese una descripción más completa</small>";

        return false;
    }

        productoDescripcion.classList.remove("is-invalid");
        productoDescripcion.classList.add("is-valid");

        errorDescripcion.innerHTML = "";
 
        return true;
    }

    // Funcion que valida que el usuario seleccione una categoría.
    function validarCategoria() {

    if (productoCategoria.value === "") {

        productoCategoria.classList.add("is-invalid");
        productoCategoria.classList.remove("is-valid");

        errorCategoria.innerHTML =
            "<small class='text-danger'>Seleccione una categoría</small>";

        return false;
    }
    // Marca el campo como válido y elimina mensajes de error..
        productoCategoria.classList.remove("is-invalid");
        productoCategoria.classList.add("is-valid");

        errorCategoria.innerHTML = "";

        return true;
    }

    // Eventos de validacion en tiempo real
    productoNombre.addEventListener("input", validarNombre);
    productoNombre.addEventListener("blur", validarNombre);

    productoDescripcion.addEventListener("input", validarDescripcion);
    productoDescripcion.addEventListener("blur", validarDescripcion);

    productoCategoria.addEventListener("change", validarCategoria);
    productoCategoria.addEventListener("blur", validarCategoria);

    // Capturar el evento submit del formulario usando addEventListener
    formProducto.addEventListener("submit", function(evento) {

    // Evita que la página se recargue al enviar el formulario
    evento.preventDefault();

    // Obtener los valores escritos por el usuario
    const nombre = productoNombre.value.trim();
    const descripcion = productoDescripcion.value.trim();
    const categoria = productoCategoria.value.trim();

    // Ejecuta todas las validaciones antes de registrar
    const nombreValido = validarNombre();
    const descripcionValida = validarDescripcion();
    const categoriaValida = validarCategoria();

    // Verifica si existe algún error
    if (!nombreValido || !descripcionValida || !categoriaValida) {

        mensajeProducto.innerHTML = `
            <div class="alert alert-danger">
                Existen errores en el formulario.
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

    // Mostrar mensaje dinámico de éxito
    mensajeProducto.innerHTML = `
        <div class="alert alert-success">
            Producto registrado correctamente.
        </div>
    `;

    // Limpiar formulario
    formProducto.reset();

    // Funcion quee limpia los mensajes de validación
    errorNombre.innerHTML = "";
    errorDescripcion.innerHTML = "";
    errorCategoria.innerHTML = "";

    // Elimina los estilos de validación después de limpiar el formulario
    productoNombre.classList.remove("is-valid");
    productoDescripcion.classList.remove("is-valid");
    productoCategoria.classList.remove("is-valid");
});