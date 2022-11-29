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

document.getElementById("buscarDocs").addEventListener('click', function (e) {
    
    Swal.fire({
        title: 'Buscando Logs....',
        timerProgressBar: true,
        didOpen: () => {
            Swal.showLoading()
            // getProcesedDocs();
            getLogs();
            // getProcesedDocs();


        },
  
    })
    e.preventDefault();
    e.stopImmediatePropagation();

})

function getLogs(params) {
    const url = new URL('http://localhost:8000/logs/');
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
                    text: 'No se han encontrado logs..',
                    showConfirmButton: false,
                    timer: 2000
                })
            }
            else {
                response.json().then(docs => {
                    logs = docs.results
                    Array.isArray(logs) ? logs.map(doc => createRowDoc(doc)) : createRowDoc(logs);                
                })

            }
        });

}

function createRowDoc(doc) 
{
    // console.log(doc.uuid);
    console.log(doc)

    const tbody = document.querySelector("#tbl-content");
    let body = '';
    let clase = "centrado";

    let tdId = `<td class = "${clase}" name = "idlog" data-label="ID log">${doc.id}</td>`,
        tdIdUsu = `<td class = "${clase}"  data-label="ID usuario">${doc.id_user}</td>`,
        tdCli = `<td class = "${clase}" data-label="Cliente">${doc.cliente}</td>`,
        tdSta = `<td class = "${clase}" data-label="Status code">${doc.status_code}</td>`,
        tdFch = `<td class = "${clase}" data-label="Fecha">${doc.fecha}</td>`;

    body += `<tr">${tdId}${tdIdUsu}${tdCli}${tdSta}${tdFch}</tr>`;
    tbody.innerHTML += body;
     
}