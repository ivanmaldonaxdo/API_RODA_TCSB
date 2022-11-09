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
document.getElementById("processDocs").addEventListener('click', function (e) {
    let folio = document.getElementById("folio").value,
        servicio = document.getElementById("tipo_servicio").value
    // console.log(folio);
    // console.log(servicio);
    if (servicio =="Tipo de servicio"  && folio == ""){
        console.log("NADA DE INFO");
    }
    else{
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
                getDocs(folio, servicio);
            },
      
        })
        
    }
    e.preventDefault();
    e.stopImmediatePropagation();

})

function numberRange (start, end) {
    return new Array(end - start).fill().map((d, i) => i + start);
}
function getDocs(folio,tpServicio, rutCli = null ) {
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
            "rut_receptor": rutCli
        })

    })
    .then((response) => {
        const status_code = response.status;
        console.log("Codigo estado es: ", response.status);
      
    
        swal.close()
        clearTable()
        if (status_code >= 400 ){
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
                Array.isArray(docs) ? docs.map(doc =>  createRowDoc(doc)) : createRowDoc(docs);
            })
            
        }
     });

}


//onclick="myFunction(this)"
// function myFunction()
function getIndexTR(x) {
    let index_tb = x.rowIndex;
    let conteo_celdas_filas = document.getElementById("tablaJS").firstElementChild.childElementCount,
        elemento = document.getElementById("tablaJS").firstElementChild;
    let items_tr = x.cells[conteo_celdas_filas-1];
    // console.log(items_tr[3]);
    let row_uuid = document.getElementsByName("uuid").item(index_tb).value,
        row_nomDoc = document.getElementsByName("nomDoc").item(index_tb).value,
        row_RutEmi = document.getElementsByName("RutEmi").item(index_tb).value;
    // console.log("uuid: ", row_uuid ," - nomDoc: ", row_nomDoc, " - RutEmi: ",row_RutEmi);

    const documento = {uuid :row_uuid , nomDoc : row_nomDoc, rut_emisor: row_RutEmi};

    Swal.fire({
        title: 'Procesando documento....',
        timerProgressBar: true,
        didOpen: () => {
            Swal.showLoading()
            contenido = downloadDocs(index_tb,documento);
            console.log(contenido);
        },
  
    })

}


function downloadDocs(index_row,documento){
    console.log("Index :", index_row);
    console.log("Objeto", documento.uuid);
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
            if (status_code >= 400 ){
                // console.log( response.json().catch(err => console.error(err)));
                // console.log("No se ha encontrado informacion");
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
            }else{
                Swal.fire({
                    // position: 'top-end',
                    icon: 'success',
                    title: 'Documento procesado con éxito',
                    showConfirmButton: false,
                    timer: 3000
                })
                deleteRow(index_row);

            }

            console.log("Contenido adquirido");
        //    console.log(response.json().MessagePort);
           return content;
        })
    });
}  


//FUNCION QUE TOMA POR PARAMETRO DOCUMENTO PARA MOSTRAR EN UNA FILA DE LA TABLA
function createRowDoc(doc,event) 
{
    // console.log(doc.uuid);
    const tbody = document.querySelector("#tablaJS");
    let body = '';
    let clase = "centrado",
        cssButton = "buttonDownload";
    // console.log(data_value);
    let btn_uuid   = `<input type="hidden" id = "uuid"   name="uuid" value="${doc.uuid}"/>`,
        btn_nomDoc = `<input type="hidden" id = "nomDoc" name="nomDoc" value="${doc.nomDoc}"/>`,
        btn_RutEmi = `<input type="hidden" id = "RutEmi" name="RutEmi" value="${doc.rut_emisor}"/>`;
    let button = `<button id = 'process-doc' class="${cssButton}" type = 'button' >Procesar</button>`;
    // let button = `<button id = 'process-doc' class="${cssButton}" type = 'button' onclick ="downloadDocs(this)">Procesar</button>`;
    
    let form_procesar = `<form action="">${btn_uuid}${btn_nomDoc}${btn_RutEmi}${button}</form>`;
    let tdfolio = `<td class = "${clase}" data-label="Folio"> ${doc.folio}</td>`,
        tdnomDoc = `<td class = "${clase}" data-label="Nombre archivo"> ${doc.nomDoc}</td>`,
        tdRutReceptor = `<td class = "${clase}" data-label="Rut cliente"> ${doc.rut_receptor}</td>`,
        tdTpServicio = `<td class = "${clase}" data-label="Tipo Servicio"> ${doc.tipo_servicio}</td>`,
        tdProcesar = `<td class = "${clase}" data-label="Procesar"> ${form_procesar}</td>`;

    body += `<tr onclick = "getIndexTR(this)">${tdfolio}${tdnomDoc}${tdRutReceptor}${tdTpServicio}${tdProcesar}</tr>`;
    tbody.innerHTML += body;
    
}
function clearTable(){
    const table = document.querySelector("#tablaJS");
    table.innerHTML = '';
}
function deleteRow(indexRow){
    // document.getElementsByTagName("tr")[indexRow].remove();
    document.getElementById("tableProcesados").deleteRow(indexRow);
    console.log("FILA ELIMINADA GG");
}

//referencias js
//https://stackoverflow.com/questions/68933909/how-to-pass-hidden-field-in-table-and-return-the-value-in-jquery-on-tr-click
//https://bobbyhadz.com/blog/javascript-map-is-not-a-function#:~:text=The%20"TypeError%3A%20map%20is%20not,of%20how%20the%20error%20occurs.
