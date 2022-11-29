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
        id: getTextElement('idsucu', indexRow),
    };
    localStorage.setItem('Idsucursal', user.id);
}

function btnDesactivar(elem) {
    let fila = elem.parentNode.parentNode.parentNode;
    let indexRow = fila.rowIndex
    const user = {
        id: getTextElement('idsucu', indexRow),
        estado: getTextElement('stateclient', indexRow)
    };
    desactivarsucu(user.id, user.estado)
}

function format(value) {
    if (value == 'Si') {
        return 'Desactivar'
    } else {
        return 'Activar'
    }
}

function desactivarsucu(id, estado) {
    Swal.fire({
        title: format(estado) + ' sucursal ?',
        type: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#3085d6',
        cancelButtonColor: '#d33',
        confirmButtonText: 'OK',
        closeOnConfirm: true,
        closeOnCancel: true
    }).then((result) => {
        if (result.value == true) {
            const url = 'http://localhost:8000/sucursales/' + id + '/'
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
                            title: 'Sucursal Desactivada correctamente',
                            icon: 'success',
                        })
                    } else if (response.status == 202) {
                        Swal.fire({
                            title: 'Sucursal Desactivada correctamente',
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

document.getElementById("buscarsucu").addEventListener('click', function(e) {
    let sucursales = document.getElementById('sucursales').value;
    if (sucursales == "") {
        Swal.fire({
            title: 'Buscando sucursales....',
            timerProgressBar: true,
            didOpen: () => {
                Swal.showLoading()
                getsucursales();
            },

        })
    } else {
        const paramsSearch = {
            nom_cli__contains: sucursales
        }

        Swal.fire({
            title: 'Buscando sucursales....',
            timerProgressBar: true,
            didOpen: () => {
                Swal.showLoading()

                getsucursales(paramsSearch);
            },

        })

    }

    e.preventDefault();
    e.stopImmediatePropagation();

})

function getsucursales(paramsURL) {
    const url = new URL('http://localhost:8000/sucursales/');
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
                text: 'No se han encontrado sucursales..',
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

function createRowDoc(doc) {

    const tbody = document.querySelector("#tbodyProcessed");
    let body = '';
    let clase = "centrado",
        cssButton = "buttonDownload";

    let btnModificar = `<button id = "idmodificar" class="${cssButton}" type="button" onclick = "btngetid(this)"> Modificar</button>`;
    let hrefModificar = `<a href = "http://localhost:8000/modificarSucursales/">${btnModificar}</a>`;
    let btnEliminar = `<button id = "ideliminar" class="${cssButton}" type="button" onclick = "btnDesactivar(this)"> Modificar</button>`;
    let hrefEliminar = `<a href = "#">${btnEliminar}</a>`;


    function validate_state(value) {
        if (value) {
            return 'Activo'
        } else {
            return 'Desactivado'
        }
    }

    let tdid = `<td class = "${clase}" name = "idsucu" data-label="Idsucursal" hidden>${doc.id}</td>`,
        tdnom_sucursal = `<td class = "${clase}" name = "nomcli" data-label="nom_sucursal">${doc.nom_sucursal}</td>`,
        tdcod = `<td class = "${clase}"  data-label="Email">${doc.cod}</td>`,
        tddireccion = `<td class = "${clase}" data-label="Razon">${doc.direccion}`,
        tdcomuna = `<td class = "${clase}" data-label="Razon">${doc.comuna}`,
        tdcliente = `<td class = "${clase}" name="" data-label="cliente">${(doc.cliente)}</td>`,
        tdmodificar = `<td class = "${clase}" data-label="Modificar">${hrefModificar}</td>`,
        tdeliminar = `<td class = "${clase}" data-label="Modificar">${hrefEliminar} </td>`,
        tdActivo = `<td class = "${clase}" name="stateclient" data-label="Estado">${validate_state(doc.is_active)}</td>`;

    body += `<tr>${tdid}${tdnom_sucursal}${tdcod}${tddireccion}${tdcomuna}${tdcliente}${tdActivo}${tdmodificar}${tdeliminar} </tr>`;
    tbody.innerHTML += body;

}

function clearTable() {
    const table = document.querySelector("#tbodyProcessed");
    table.innerHTML = '';
}