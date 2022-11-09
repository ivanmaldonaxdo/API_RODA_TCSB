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
    // const url = 'http://3.80.228.126/procesados/
    const url = 'http://localhost:8000/procesados/';
    fetch(url, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
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

//FUNCION QUE TOMA POR PARAMETRO DOCUMENTO PARA MOSTRAR EN UNA FILA DE LA TABLA
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

    let btnDownload = `<button id = "downloadDoc" class="${cssButton}" type="button"> Descargar</button>`;
    let hrefDownload = `<a href = "${urlBase}}${doc.documento}" download> ${btnDownload}</a>`;

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

//referencias js
//https://stackoverflow.com/questions/68933909/how-to-pass-hidden-field-in-table-and-return-the-value-in-jquery-on-tr-click
//https://bobbyhadz.com/blog/javascript-map-is-not-a-function#:~:text=The%20"TypeError%3A%20map%20is%20not,of%20how%20the%20error%20occurs.
