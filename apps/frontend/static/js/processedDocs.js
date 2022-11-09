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
document.getElementById("buscarDocs").addEventListener('click', function (e) {
    // let folio = document.getElementById("folio").value,
    //     servicio = document.getElementById("tipo_servicio").value
    // console.log(folio);
    // console.log(servicio);
    // if (servicio =="Tipo de servicio"  && folio == ""){
    //     console.log("NADA DE INFO");
    // }
    // else{
    //     if (servicio == "Tipo de servicio") {
    //         // console.log("servicio inservible");

    //         servicio = null;
    //     }
        
        
    // }
    Swal.fire({
        title: 'Buscando documentos procesados....',
        timerProgressBar: true,
        didOpen: () => {
            Swal.showLoading()
            getProcesedDocs();
        },
  
    })
    e.preventDefault();
    e.stopImmediatePropagation();

})


function getProcesedDocs() {
    // const url = 'http://3.80.228.126/documentos/search_docs/'
    const url = 'http://localhost:8000/procesados/';
    // const HTMLResponse = document.querySelector("#tablaJS")
    fetch(url, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        // body: JSON.stringify({
        //     "folio": folio,
        //     "tipo_servicio": tpServicio,
        //     "rut_receptor": rutCli
        // })

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
    // console.log(items_tr[3]);

    //     title: 'Procesando documento....',
    //     timerProgressBar: true,
    //     didOpen: () => {
    //         Swal.showLoading()
    //         console.log(contenido);

    //     },
  
    // })


}

//FUNCION QUE TOMA POR PARAMETRO DOCUMENTO PARA MOSTRAR EN UNA FILA DE LA TABLA
function createRowDoc(doc,event) 
{
    // console.log(doc.uuid);
    const tbody = document.querySelector("#tbodyProcessed");
    let body = '';
    let clase = "centrado",
        cssButton = "buttonDownload";
    
    // let href = `<a href = "http://localhost:8000${doc.documento}" download ></a>`
    // let button = `<button id = 'downloadDoc' class="${cssButton}" type = 'button'>${href}Descargar </button>`;
    let btnDownload = `<button onclick="location.href='http://www.example.com'" id = "downloadDoc" class="${cssButton}" type="button" download> Descargar</button>`;
    // let button = `<button id = 'process-doc' class="${cssButton}" type = 'button' onclick ="downloadDocs(this)">Procesar</button>`;

    // let form_procesar = `<form action="">${button}</form>`;
    var linkaso = `${doc.documento}`
    let tdfolio = `<td class = "${clase}" data-label="Folio">${doc.folio}</td>`,
        tdSucur = `<td class = "${clase}"  data-label="Sucursal">${doc.rut_sucursal}</td>`,
        // tdnomDoc = `<td class = "${clase}"  data-label="Sucursal">${doc.nom_doc}</td>`,
        tdFechaProcess = `<td class = "${clase}" data-label="Fecha Procesado">${doc.fecha}</td>`,
        tdDownload = `<td class = "${clase}" data-label="Documento">${btnDownload} </td>`;

        // tdDownload = `<td class = "${clase}" data-label="Documento"><a href = "http://localhost:8000${doc.documento}" download ></a>Descargar </td>`;
        // tdRutReceptor = `<td class = "${clase}">${doc.rut_receptor}</td>`,
        // tdDownload = `<td class = "${clase}">${form_procesar}</td>`;

    body += `<tr">${tdfolio}${tdSucur}${tdFechaProcess}${tdDownload}</tr>`;
    tbody.innerHTML += body;
    
}
function clearTable(){
    const table = document.querySelector("#tbodyProcessed");
    table.innerHTML = '';
}
// function deleteRow(indexRow){
//     // document.getElementsByTagName("tr")[indexRow].remove();
//     document.getElementById("tableProcesados").deleteRow(indexRow);
//     console.log("FILA ELIMINADA GG");
// }

//referencias js
//https://stackoverflow.com/questions/68933909/how-to-pass-hidden-field-in-table-and-return-the-value-in-jquery-on-tr-click
//https://bobbyhadz.com/blog/javascript-map-is-not-a-function#:~:text=The%20"TypeError%3A%20map%20is%20not,of%20how%20the%20error%20occurs.
