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
    let metodo = document.getElementById("fl_Metodo").value,
        idLog = document.getElementById("fl_IDlog").value,
        IDUser = document.getElementById("fl_IDUser").value,
        IDCli = document.getElementById("fl_IDUser").value,
        status = document.getElementById("fl_StatusCode").value,
        fecha = document.getElementById("fl_fecha").value;
    const params  = {
        method: metodo,
        id:idLog,IDUser,
        cliente:IDCli,
        status_code:status,
        fecha_hora__date:fecha
}
    //?id=&id_user=&cliente=&method=&status_code=&fecha_hora__date=
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
    const url = new URL('http://100.27.17.66/logs/');
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
        tdFch = `<td class = "${clase}" data-label="Fecha" hidden>${doc.fecha}</td>`;

    body += `<tr">${tdId}${tdIdUsu}${tdCli}${tdSta}${tdFch}</tr>`;
    tbody.innerHTML += body;
     
}