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
////////


document.getElementById("searchDocs").addEventListener('click', function (e) {

    let folio = document.getElementById("folio").value,
        servicio = document.getElementById("tipo_servicio").value
    // console.log(fecha.toLocaleDateString('es-CL'));
    // console.log(typeof fecha);
    let fecha_emision = document.querySelector('#fechaBusqueda').value;
    fecha_emision = String(fecha_emision);
    let isVacio = fecha_emision == "";
    console.log(isVacio); 
    console.log(fecha_emision);
    let rut_client = null,
        rut_receptor = null;
    // console.log(isVacio);
    // let dia = isVacio  ? null : list_fecha[0],
    //     mes = isVacio ? null : list_fecha[1],
    //     anio = isVacio  ? null: list_fecha[2];
    // console.log(dia," ",mes," ",anio);
    if (servicio == "Tipo de servicio" && folio == "" && isVacio)  {
        console.log("NADA DE INFO");
        Swal.fire({
            // title: '<strong>HTML <u>example</u></strong>',
            icon: 'info',
            html:
              'Seleccione algunos campos para buscar  <b>documentos</b>',
            showCloseButton: false,
            showCancelButton: false,
            showConfirmButton: false,
            timer: 2000
        
          })
    }
    else {
        if (servicio == "Tipo de servicio") {
            // console.log("servicio no permitido");

            servicio = null;
        }
        // Swal.fire({
        //     title: 'Are you sure?',
        //     text: "You won't be able to revert this!",
        //     icon: 'info',
        // })
        Swal.fire({
            title: 'Buscando documentos a procesar....',
            timerProgressBar: true,
            didOpen: () => {
                Swal.showLoading()
                
                getDocs(folio, servicio,rut_client, rut_receptor,fecha_emision);
            },

        })

    }

    e.preventDefault();
    e.stopImmediatePropagation();
})

function numberRange(start, end) {
    return new Array(end - start).fill().map((d, i) => i + start);
}
function getDocs(folio, tpServicio,rut_client, rut_receptor,fecha = null) {
    // const url = 'http://3.80.228.126/documentos/search_docs/'
    const url = 'http://localhost:8000/documentos/search_docs/';
    // const HTMLResponse = document.querySelector("#tablaJS")
    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({
            "folio": folio,
            "tipo_servicio": tpServicio,
            "rut_client": rut_client,
            "rut_receptor":rut_receptor,
            "fecha": fecha
        })

    })
        .then((response) => {
            const status_code = response.status;
            console.log("Codigo estado es: ", response.status);


            swal.close()
            clearTable()
            if (status_code >= 400) {
                Swal.fire({
                    icon: 'error',
                    title: 'Oops...',
                    text: 'No se han encontrado documentos..',
                    showConfirmButton: false,
                    timer: 2000
                })
                // console.log( response.json().catch(err => console.error(err)));
                // console.log("No se ha encontrado informacion");
            }
            else {
                response.json().then(docs => {
                    Array.isArray(docs) ? docs.map(doc => createRowDoc(doc)) : createRowDoc(docs);
                    console.log(docs);
                })

            }
        });

}
//"el" es elemento por ej: "uuid", index la fila en es que se encuentra
/// SIRVE PARA OBTENER VALORES DE BOTONES
let getValueElement = (el, index) => {
    return document.getElementsByName(el).item(index).value;
}

////OBTIENE EL CONTENIDO DE LOS TD (NO BOTONES)
let getTextElement = (el, index) => {
    return document.getElementsByName(el).item(index).textContent;
}

let getValueByID = (el) => {
    return document.getElementById(el).value;
}

let setValueByID = (el, newValue) => {
    document.getElementById(el).value = newValue;
}

//onclick="myFunction(this)"
// function myFunction()
function EditRecordForEditDemo(element) {
    var rowJavascript = element.parentNode.parentNode;
    var rowjQuery = $(element).closest("tr");
    alert("JavaScript Row Index : " + (rowJavascript.rowIndex - 1) + "\njQuery Row Index : " + (rowjQuery[0].rowIndex - 1));
}
//boton para abrir y cerrar detalle
function btndetalleDocs(elem) {
    let fila = elem.parentNode.parentNode.parentNode;
    let indexRow = fila.rowIndex
    console.log(indexRow);
    console.log(getValueByID("mdFolio"));
    let rut_cli = getTextElement('tdRutCli', indexRow),
        rut_proveedor = getTextElement('RutEmi', indexRow);

    console.log(rut_cli);
    // console.log(getTextElement('tdRutCli',indexRow));
    console.log(getTextElement('tdFolio', indexRow));

    //////////SETEO DE PROPIEDADES DEL MODAL EN JS
    setValueByID("mdFolio", getTextElement('tdFolio', indexRow));
    setValueByID("mdNomDoc", getValueElement('nomDoc', indexRow));
    setValueByID("mdFechaEmi", getValueElement('fechaEmi', indexRow));
    setValueByID("mdRutEmi", rut_proveedor);
    // tdRutReceptor
    // console.log(client);
    // console.log("Cliente is ", cliente);
    // setValueID("mdFolio",getValueElement("tdFolio",indexRow));

    let cerrar = document.querySelectorAll(".close")[0];
    let modal = document.querySelectorAll(".amodal")[0];
    let modalc = document.querySelectorAll(".modal-container")[0];

    modalc.style.opacity = "1";
    modalc.style.visibility = "visible";
    modal.classList.toggle("modal-close");

    getDataClient(rut_cli).then(
        client => Array.isArray(client) ? setValueByID("mdNomCli", client.map(cli => cli.nom_cli)) : client.nom_cli
    )
    getDataProv(rut_proveedor).then(
        prov => Array.isArray(prov) ? setValueByID("mdNomProv", prov.map(prv => prv.nom_proveedor)) : prov.nom_proveedor
    )
}
let cerrar = document.querySelectorAll(".close")[0];
let modal = document.querySelectorAll(".amodal")[0];
let modalc = document.querySelectorAll(".modal-container")[0];

cerrar.addEventListener("click", function () {
    modal.classList.toggle("modal-close");

    setTimeout(function () {
        modalc.style.opacity = "0";
        modalc.style.visibility = "hidden";
    }, 600);

});

window.addEventListener("click", function (e) {
    if (e.target == modalc) {
        modal.classList.toggle("modal-close");
        setTimeout(function () {
            modalc.style.opacity = "0";
            modalc.style.visibility = "hidden";
        }, 600);
    }
})

async function getDataClient(rutCliente) {
    const url = new URL("http://localhost:8000/clientes/");
    const params = { rut_cliente: rutCliente }
    url.search = new URLSearchParams(params).toString();
    const res = await fetch(url, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        }
    })
    obj = await res.json();

    return obj
}

async function getDataProv(rutProveedor) {
    const url = new URL("http://localhost:8000/proveedores/");
    const params = { rut_proveedor: rutProveedor }
    url.search = new URLSearchParams(params).toString();
    const res = await fetch(url, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        }
    })
    obj = await res.json();
    return obj
}
///////////////////////////////////////////////////////////////////


///////////PROCESAR DOCUMENT0S
function btnProcessDocs(elem) {
    let fila = elem.parentNode.parentNode.parentNode;
    let indexRow = fila.rowIndex
    const documento = {
        uuid: getValueElement('uuid', indexRow),
        nomDoc: getValueElement('nomDoc', indexRow),
        rut_emisor: getValueElement('RutEmi', indexRow),
        rut_client: getTextElement('tdRutCli', indexRow)
    };
    Swal.fire({
        title: 'Procesando documento....',
        timerProgressBar: true,
        didOpen: () => {
            Swal.showLoading()
            console.log(documento);
            contenido = processDocs(indexRow, documento);
            // console.log(contenido);            
        },

    })
}

function processDocs(indexRow, documento) {
    // console.log("Index :", indexRow);
    // console.log("Objeto", documento.uuid);
    // const url = 'http://3.80.228.126/documentos/process_docs/';
    const url = 'http://localhost:8000/documentos/process_docs/';

    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify(documento)

    })
    .then((response) => {
        response.json().then(content => {
            const status_code = response.status;
            swal.close()
            if (status_code >= 400) {
                // console.log( response.json().catch(err => console.error(err)));
                Swal.fire({
                    // position: 'top-end',
                    icon: 'error',
                    title: 'Tuvimos problemas para procesar este archivo',
                    showConfirmButton: false,
                    timer: 3000
                })

                // Swal.fire({
                //     icon: 'error',
                //     title: 'Oops...',
                //     text: 'No se han encontrado documentos..',
                //     // footer: '<a href="">Why do I have this issue?</a>'
                // })
            } else {
                Swal.fire({
                    // position: 'top-end',
                    icon: 'success',
                    title: 'Documento procesado con éxito',
                    showConfirmButton: false,
                    timer: 3000
                })
                deleteRow(indexRow);

            }
            console.log("Contenido adquirido");
            return content;
        })
        .catch(err => {
            console.log('caught it!', err);
        });
    });
}


//FUNCION QUE TOMA POR PARAMETRO DOCUMENTO PARA MOSTRAR EN UNA FILA DE LA TABLA
function createRowDoc(doc, event) {
    const tbody = document.querySelector("#tablaJS");
    let body = '';
    let clase = "centrado",
        cssButton = "buttonDownload";
    // console.log(data_value);
    var fechaEmi = `${doc.dia_doc}/${doc.mes_doc}/${doc.anio_doc}`
    let btn_uuid = `<input type="hidden" id = "uuid"   name="uuid" value="${doc.uuid}"/>`,
        btn_nomDoc = `<input type="hidden" id = "nomDoc" name="nomDoc" value="${doc.nomDoc}"/>`,
        btn_RutRecep = `<input type="hidden" id = "RutRecep" name="RutRecep" value="${doc.rut_receptor}"/>`;

    let btnProcesar = `<button id = 'process-doc' class="${cssButton}" type = 'button' name="process-doc" onclick = "btnProcessDocs(this)">Procesar</button>`,
        btnDetalle = `<button id = 'detalleDoc' class="${cssButton}" type = 'button' name="detalleDoc" onclick = "btndetalleDocs(this)">Detalle</button>`,
        btnFechaEmi = `<input type="hidden" id = "fechaEmi" name="fechaEmi" value="${fechaEmi}"/>`,
        btn_RutEmi = `<input type="hidden" id = "RutEmi" name="RutEmi" value="${doc.rut_emisor}"/>`;

    // let button = `<button id = 'process-doc' class="${cssButton}" type = 'button' onclick ="downloadDocs(this)">Procesar</button>`;
    //////////// FORMS PARA BOTONES
    let form_detalle = `<form action="">${btnDetalle}${btnFechaEmi}${btn_RutEmi}</form>`;
    let form_procesar = `<form action="">${btn_uuid}${btn_nomDoc}${btn_RutRecep}${btnProcesar}</form>`;


    let tdfolio = `<td class = "${clase}" data-label="Folio" name ="tdFolio"> ${doc.folio}</td>`,
        tdRutClient = `<td class = "${clase}" data-label="Rut cliente" name ="tdRutCli">${doc.rut_client}</td>`,
        tdTpServicio = `<td class = "${clase}" data-label="Tipo Servicio"> ${doc.tipo_servicio}</td>`,
        tdProcesar = `<td class = "${clase}" data-label="Procesar"> ${form_procesar}</td>`,
        tdDetalle = crearTd(clase, "Detalle", form_detalle);

    // tdDetalle = `<td class = "${clase}" data-label="Detalle"> ${form_detalle}</td>`;

    body += `<tr>${tdfolio}${tdRutClient}${tdTpServicio}${tdProcesar}${tdDetalle}</tr>`;
    tbody.innerHTML += body;

}

function crearTd(clase, dt_label, contenido) {
    let td = `<td class = "${clase}" data-label="${dt_label}"> ${contenido}</td>`;
    return td
}
function clearTable() {
    const table = document.querySelector("#tablaJS");
    table.innerHTML = '';
}
function deleteRow(indexRow) {
    // document.getElementsByTagName("tr")[indexRow].remove();
    document.getElementById("tableProcesados").deleteRow(indexRow);
    console.log("FILA ELIMINADA GG");
}

//referencias js
//https://stackoverflow.com/questions/68933909/how-to-pass-hidden-field-in-table-and-return-the-value-in-jquery-on-tr-click
//https://bobbyhadz.com/blog/javascript-map-is-not-a-function#:~:text=The%20"TypeError%3A%20map%20is%20not,of%20how%20the%20error%20occurs.

