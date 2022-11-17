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


//funcion para detener el proceso


//funcion para procesar archivos por folio
//muestraproce
document.getElementById("muestraproce").addEventListener('click', function (e) {
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

document.getElementById("muestraproce").addEventListener('click', function (e) {
    let folio = document.getElementById("folio").value
        //servicio = document.getElementById("tipo_servicio").value
        // console.log(folio);
        // console.log(servicio);
    if (servicio =="Tipo de servicio" && folio == ""){
        console.log("NADA DE INFO");
    }
    else{
        if (servicio == "Tipo de servicio") {
            // console.log("servicio no permitido");
            servicio = null;
        }
            //si campos vacios se ejecuta codigo arrida de lo contrario
            //se ejecuta el codigo de abajo solo por folio
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

//se manda a llamar la funcion getdocs solo ingresando el folio 
//para pronto asociarlo a al tipo de servicio
function getDocs(folio,tpServicio, rutCli = null ) {
    //en esta URL se consume las funciones de cron basado
    const url = 'http://localhost:8000/documentos/procesocompleto/';
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
        }
        else {
            response.json().then(docs => {
                Array.isArray(docs) ? docs.map(doc =>  createRowDoc(doc)) : createRowDoc(docs);
            })
            
        }
     });

}


function createRowDoc(doc,event) 
{
    // console.log(doc.uuid);
    const tbody = document.querySelector("#tbodyProcessed");
    let body = '';
    let clase = "centrado",
        cssButton = "buttonDownload";
    
    //LOCAL
    var urlBase = 'http://localhost:8000';
    //server
    // var urlBase = 'http://localhost'
    var urlDownload = urlBase + doc.documento

    let btnDownload = `<button id = "downloadDoc" class="${cssButton}" type="button"> Descargar</button>`;
    let hrefDownload = `<a href = "${urlDownload}" download> ${btnDownload}</a>`;

    let tdfolio = `<td class = "${clase}" data-label="Folio">${doc.folio}</td>`,
        tdSucur = `<td class = "${clase}"  data-label="Sucursal">${doc.rut_sucursal}</td>`,
        tdFechaProcess = `<td class = "${clase}" data-label="Fecha Procesado">${doc.fecha}</td>`,
        tdDownload = `<td class = "${clase}" data-label="Documento">${hrefDownload} </td>`;



    body += `<tr">${tdfolio}${tdSucur}${tdFechaProcess}${tdDownload}</tr>`;
    tbody.innerHTML += body;
    
}
function clearTable(){
    const table = document.querySelector("#tbodyProcessed");
    table.innerHTML = '';
}




