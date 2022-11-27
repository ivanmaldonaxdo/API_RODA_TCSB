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
        didOpen: () => {
            Swal.showLoading()
            // getProcesedDocs();
            getSucursal();
            // getProcesedDocs();
        },
  
    })
    e.preventDefault();
    e.stopImmediatePropagation();

})


function getSucursal() {
    const url ='http://localhost:8000/sucursales/';
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