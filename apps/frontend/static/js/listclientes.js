function getCookie(cname) {
    var name = cname + "=";
    var decodedCookie = decodeURIComponent(document.cookie);
    var ca = decodedCookie.split(';');
    for(var i = 0; i <ca.length; i++) {
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
        id: getTextElement('idclient', indexRow),
    };
    localStorage.setItem('Idcliente', user.id);
}

function btnDesactivar(elem) {
    
    let fila = elem.parentNode.parentNode.parentNode;
    let indexRow = fila.rowIndex
    const user = {
        id: getTextElement('idclient', indexRow),
        estado: getTextElement('stateclient', indexRow)
    };
    desactivarClient(user.id, user.estado)
}

function format(value){
    if (value=='Si'){
        return 'Desactivar'
    }else{
        return 'Activar'
    }
}

function desactivarClient(id, estado){
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
        if (result.value==true) {
            const url = 'http://localhost:8000/clientes/'+id+'/'
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
                            title:'Cliente Desactivado correctamente',
                            icon:'success',
                        })
                    }
                    else if (response.status==202) {
                        Swal.fire({
                            title:'Cliente Activado correctamente',
                            icon:'success',
                        })
                    
                    }else{
                        Swal.fire({
                            title:'Error al intentar la operacion',
                            icon:'success',
                        })
                    }
                })
            })
        }
    })
}

document.getElementById("buscarDocs").addEventListener('click', function (e) {
    let nom_cli = document.getElementById('clientes').value;
    if(nom_cli == ""){
            Swal.fire({
            title: 'Buscando Clientes....',
            timerProgressBar: true,
            didOpen: () => {
                Swal.showLoading()
                // getProcesedDocs();
                getClientes();
                // getProcesedDocs();
            },
    
        })
    }
    else {
        const paramsSearch =  { 
            nom_cli__contains:nom_cli
            }
        
        Swal.fire({
            title: 'Buscando clientes....',
            timerProgressBar: true,
            didOpen: () => {
                Swal.showLoading()
                
                getClientes(paramsSearch);
            },

        })

    }
    
    e.preventDefault();
    e.stopImmediatePropagation();

})

function getSucursal(paramsURL) {
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

            if (status_code >= 400) {
                Swal.fire({
                    icon: 'error',
                    title: 'Oops...',
                    text: 'No se han encontrado sucursales..',
                    showConfirmButton: false,
                    timer: 2000
                })
            }
            else {
                response.json().then(docs => {
                    Array.isArray(docs) ? docs.map(doc => createRowDocSuc(doc)) : createRowDocSuc(docs);
                })

            }
        });

}

function getClientes(paramsURL) {
    const url = new URL('http://localhost:8000/clientes/');
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
            }
            else {
                response.json().then(docs => {
                    Array.isArray(docs) ? docs.map(doc => createRowDoc(doc)) : createRowDoc(docs);
                })

            }
        });

}

function createRowDoc(doc) 
{
    // console.log(doc.uuid);
    const tbody = document.querySelector("#tbodyProcessed");
    let body = '';
    let clase = "centrado",
        cssButton = "buttonDownload";

    let btnModificar = `<button id = "idmodificar" class="${cssButton}" type="button" onclick = "btngetid(this)"> Modificar</button>`;
    let hrefModificar = `<a href = "http://localhost:8000/Modificarcliente/">${btnModificar}</a>`;
    let btnEliminar = `<button id = "ideliminar" class="${cssButton}" type="button" onclick = "btnDesactivar(this)"> Modificar</button>`;
    let hrefEliminar = `<a href = "#">${btnEliminar}</a>`;

    function validate_state(value){
        if (value) {
            return 'Activo'
        }
        else {
            return 'Desactivado'
        }
    }

    let tdId = `<td class = "${clase}" name = "idclient" data-label="Idcliente">${doc.id}</td>`,
        tdNom = `<td class = "${clase}" name = "nomcli" data-label="nomcli">${doc.nom_cli}</td>`,
        tdRut = `<td class = "${clase}"  data-label="Email">${doc.rut_cliente}</td>`,
        tdRazon = `<td class = "${clase}" data-label="Razon">${doc.razon_social}`,
        tdActivo = `<td class = "${clase}" name="stateclient" data-label="Estado">${validate_state(doc.is_active)}</td>`,
        tdmodificar = `<td class = "${clase}" data-label="Modificar">${hrefModificar}</td>`,
        tdeliminar = `<td class = "${clase}" data-label="Modificar">${hrefEliminar} </td>`;



    body += `<tr">${tdId}${tdNom}${tdRut}${tdRazon}${tdActivo}${tdmodificar}${tdeliminar}</tr>`;
    tbody.innerHTML += body;
    const paramsSearch =  { 
        cliente:doc.id
        }

    getSucursal(paramsSearch);
    
}

function createRowDocSuc(doc) 
{
    // console.log(doc.uuid);
    const tbody = document.querySelector("#tbodySucursales");
    let body = '';
    let clase = "centrado";

    let tdNom_suc = `<td class = "${clase}" name = "nom_sucursal" data-label="nomcli">${doc.nom_sucursal}</td>`,
        tdDir = `<td class = "${clase}"  data-label="Direccion">${doc.direccion}</td>`,
        tdCom = `<td class = "${clase}" data-label="comuna">${doc.comuna}`,
        tdCon = `<td class = "${clase}" name="cliente" data-label="cliente">${doc.cliente}</td>`;

    body += `<tr">${tdNom_suc}${tdDir}${tdCom}${tdCon}</tr>`;
    tbody.innerHTML += body;
     
    
}


function clearTable(){
    const table = document.querySelector("#tbodyProcessed");
    table.innerHTML = '';
}