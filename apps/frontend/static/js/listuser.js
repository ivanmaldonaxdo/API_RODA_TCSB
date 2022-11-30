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
        id: getTextElement('iduser', indexRow),
    };
    localStorage.setItem('idusuario', user.id);
}

function btnDesactivar(elem) {
    
    let fila = elem.parentNode.parentNode.parentNode;
    let indexRow = fila.rowIndex
    const user = {
        id: getTextElement('iduser', indexRow),
        estado: getTextElement('stateuser', indexRow)
    };
    desactivarUser(user.id, user.estado)
}

function format(value){
    if (value=='Si'){
        return 'Desactivar'
    }else{
        return 'Activar'
    }
}

function desactivarUser(id, estado){
    Swal.fire({
        title: format(estado) + ' Usuario?',
        type: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#3085d6',
        cancelButtonColor: '#d33',
        confirmButtonText: 'OK',
        closeOnConfirm: true,
        closeOnCancel: true
    }).then((result) => {
        if (result.value==true) {
            const url = 'http://3.239.229.60/usuarios/'+id+'/'
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
                            title:'Usuario Desactivado correctamente',
                            icon:'success',
                        })
                    }
                    else if (response.status==202) {
                        Swal.fire({
                            title:'Usuario Activado correctamente',
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
    Swal.fire({
        title: 'Buscando Usuarios....',
        timerProgressBar: true,
        didOpen: () => {
            Swal.showLoading()
            // getProcesedDocs();
            getUsuarios();
            // getProcesedDocs();


        },
  
    })
    e.preventDefault();
    e.stopImmediatePropagation();

})


function getUsuarios() {
    const url = 'http://3.239.229.60/usuarios/';
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
            clearTable()
            if (status_code >= 400) {
                Swal.fire({
                    icon: 'error',
                    title: 'Oops...',
                    text: 'No se han encontrado usuarios..',
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


//FUNCION QUE TOMA POR PARAMETRO DOCUMENTO PARA MOSTRAR EN UNA FILA DE LA TABLA
function createRowDoc(doc) 
{
    // console.log(doc.uuid);
    const tbody = document.querySelector("#tbodyProcessed");
    let body = '';
    let clase = "centrado",
        cssButton = "buttonDownload";
    console.log(doc)

    let btnModificar = `<button id = "idmodificar" class="${cssButton}" type="button" onclick = "btngetid(this)"> Modificar</button>`;
    let hrefModificar = `<a href = "http://3.239.229.60/Modificarusuario/">${btnModificar}</a>`;
    let btnEliminar = `<button id = "ideliminar" class="${cssButton}" type="button" onclick = "btnDesactivar(this)"> Modificar</button>`;
    let hrefEliminar = `<a href = "#">${btnEliminar}</a>`;

    function validate_state(value){
        if (value) {
            return 'Si'
        }
        else {
            return 'No'
        }
    }

    let tdId = `<td class = "${clase}" name = "iduser" data-label="Idusuario">${doc.id}</td>`,
        tdEmail = `<td class = "${clase}"  data-label="Email">${doc.email}</td>`,
        tdActivo = `<td class = "${clase}" name="stateuser" data-label="Estado">${validate_state(doc.is_active)}</td>`,
        tdmodificar = `<td class = "${clase}" data-label="Modificar">${hrefModificar}</td>`,
        tdeliminar = `<td class = "${clase}" data-label="Modificar">${hrefEliminar} </td>`;



    body += `<tr">${tdId}${tdEmail}${tdActivo}${tdmodificar}${tdeliminar}</tr>`;
    tbody.innerHTML += body;
    
}
function clearTable(){
    const table = document.querySelector("#tbodyProcessed");
    table.innerHTML = '';
}

