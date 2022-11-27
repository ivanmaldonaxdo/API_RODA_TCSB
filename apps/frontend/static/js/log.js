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

function getLogs() {
    const url ='http://localhost:8000/logs/';
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
                    Array.isArray(docs) ? docs.map(doc =>Array.from(doc.results).map(d=>createRowDoc(d))) : createRowDoc(docs);
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

    let tdId = `<td class = "${clase}" name = "idlog" data-label="idlog">${doc.id}</td>`,
        tdIdUsu = `<td class = "${clase}"  data-label="iduser">${doc.id_user}</td>`,
        tdApi = `<td class = "${clase}" data-label="api">${doc.api}`,
        tdCli = `<td class = "${clase}" name="cliente" data-label="cliente">${doc.cliente}</td>`,
        tdPay = `<td class = "${clase}" name="payload" data-label="payload">${doc.payload}</td>`,
        tdSta = `<td class = "${clase}" name="status" data-label="status">${doc.status_code}</td>`,
        tdFch = `<td class = "${clase}" name="fechahora" data-label="fechahora">${doc.fecha_hora}</td>`,
        tdRes = `<td class = "${clase}" name="response" data-label="response">${doc.response}</td>`;

    body += `<tr">${tdId}${tdIdUsu}${tdApi}${tdCli}${tdPay}${tdSta}${tdFch}${tdRes}</tr>`;
    tbody.innerHTML += body;
     
}