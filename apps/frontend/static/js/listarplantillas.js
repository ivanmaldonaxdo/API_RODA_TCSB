function getCookie(cname) {
    var name = cname + "=";
    var decodedCookie = decodeURIComponent(document.cookie);
    var ca = decodedCookie.split(';');
    for (var i = 0; i < ca.length; i++) {
        var c = ca[i];
        while (c.charAt(0) == ' ') {
            c = c.substring(1);
        }
        if (c.indexOf(name) == 0) {
            return c.substring(name.length, c.length);
        }
    }
    return "";
}
var csrftoken = getCookie('csrftoken');

let getValueElement = (el, index) => {
    return document.getElementsByName(el).item(index).value;
}

let getTextElement = (el, index) => {
    return document.getElementsByName(el).item(index).textContent;
}

function btngetid(elem) {
    let fila = elem.parentNode.parentNode.parentNode;
    let indexRow = fila.rowIndex
    const user = {
        id: getTextElement('idplant', indexRow),
    };
    localStorage.setItem('Idplantilla', user.id);
}

function btnDesactivar(elem) {

    let fila = elem.parentNode.parentNode.parentNode;
    let indexRow = fila.rowIndex
    const user = {
        id: getTextElement('idplant', indexRow),
        estado: getTextElement('stateclient', indexRow)
    };
    desactivarClient(user.id, user.estado)
}

function format(value) {
    if (value == 'Si') {
        return 'Desactivar'
    } else {
        return 'Activar'
    }
}
//eliminar supuesto cliente/sucursal
//plantilla no tiene estado is:active
function desactivarClient(id, estado) {
    Swal.fire({
        title: format(estado) + ' Cliente?',
        type: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#3085d6',
        cancelButtonColor: '#d33',
        confirmButtonText: 'OK',
        closeOnConfirm: true,
        closeOnCancel: true
    }).then((result) => {
        if (result.value == true) {
            const url = 'http://localhost:8000/clientes/' + id + '/'
            fetch(url, {
                method: 'DELETE',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrftoken,
                },
            }).then((response) => {
                response.json().then(data => {
                    if (response.status == 200) {
                        Swal.fire({
                            title: 'Cliente Desactivado correctamente',
                            icon: 'success',
                        })
                    } else if (response.status == 202) {
                        Swal.fire({
                            title: 'Cliente Activado correctamente',
                            icon: 'success',
                        })

                    } else {
                        Swal.fire({
                            title: 'Error al intentar la operacion',
                            icon: 'success',
                        })
                    }
                })
            })
        }
    })
}

document.getElementById("buscarplantilla").addEventListener('click', function(e) {
    let plantilla = document.getElementById('plantillas').value;
    if (plantilla == "") {
        Swal.fire({
            title: 'Buscando Plantillas....',
            timerProgressBar: true,
            didOpen: () => {
                Swal.showLoading()
                    // getProcesedDocs();
                getplantillas();
                // getProcesedDocs();
            },

        })
    } else {
        const paramsSearch = {
            nom_cli__contains: plantilla
        }

        Swal.fire({
            title: 'Buscando Plantillas....',
            timerProgressBar: true,
            didOpen: () => {
                Swal.showLoading()
                getplantillas(paramsSearch);
            },

        })

    }

    e.preventDefault();
    e.stopImmediatePropagation();

})


function getplantillas(paramsURL) {
    const url = new URL('http://localhost:8000/plantillas/');
    const params = paramsURL;
    url.search = new URLSearchParams(params).toString();
    fetch(url, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
    }).then((response) => {
        const status_code = response.status;
        console.log("Codigo estado es: ", response.status);


        swal.close()
        const table = document.querySelector("#tbodyProcessed");
        table.innerHTML = '';
        if (status_code >= 400) {
            Swal.fire({
                icon: 'error',
                title: 'Oops...',
                text: 'No se han encontrado plantillas..',
                showConfirmButton: false,
                timer: 2000
            })
        } else {
            response.json().then(docs => {
                Array.isArray(docs) ? docs.map(doc => createRowDoc(doc)) : createRowDoc(docs);
            })

        }
    });

}

//id
//<th class="centrado">nom_doc</th>
//<th class="centrado">queries_config</th>
//<th class="centrado">tablas_config</th>

//<th class="centrado">fecha_creacion</th>
//<th class="centrado">proveedor</th>


function createRowDoc(doc) {

    const tbody = document.querySelector("#tbodyProcessed");
    let body = '';
    let clase = "centrado",
        cssButton = "buttonDownload";

    let btnModificar = `<button id = "idmodificar" class="${cssButton}" type="button" onclick = "btngetid(this)"> Modificar</button>`;
    let hrefModificar = `<a href = "http://localhost:8000/modificarplantilla/">${btnModificar}</a>`;
    //let btnEliminar = `<button id = "ideliminar" class="${cssButton}" type="button" onclick = "btnDesactivar(this)"> Modificar</button>`;
    //let hrefEliminar = `<a href = "#">${btnEliminar}</a>`;

    function validate_state(value) {
        if (value) {
            return 'Activo'
        } else {
            return 'Desactivado'
        }
    }

    //tdqueries_config = `<td class = "${clase}"  data-label="queries_config">${doc.queries_config}</td>`${tdqueries_config} ,
    // tdtablas_config = `<td class = "${clase}" data-label="tablas_config">${doc.tablas_config}`    ${tdtablas_config},

    let tdid = `<td class = "${clase}" name = "idplant" data-label="Idplantilla" hidden >${doc.id}</td>`,
        tdnom_doc = `<td class = "${clase}" name = "nomcli" data-label="nom_doc">${doc.nom_doc}</td>`,
        tdfecha_creacion = `<td class = "${clase}" datetime="fecha_creacion">${doc.fecha_creacion}`,
        tdproveedor = `<td class = "${clase}" data-label="proveedor">${doc.proveedor}`,
        tdmodificar = `<td class = "${clase}" data-label="Modificar">${hrefModificar}</td>`;

    body += `<tr>${tdid}${tdnom_doc}${tdfecha_creacion}${tdproveedor}${tdmodificar}</tr>`;

    tbody.innerHTML += body;

}

function clearTable() {
    const table = document.querySelector("#tbodyProcessed");
    table.innerHTML = '';
}