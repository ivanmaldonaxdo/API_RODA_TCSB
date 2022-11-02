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

// let folio = 11419589
// let tpServicio = null
// let rut = null
document.getElementById("processDocs").addEventListener('click', function (e) {
    let folio = document.getElementById("folio").value,
        servicio = document.getElementById("tipo_servicio").value
    e.preventDefault()
    console.log(folio)
    console.log(servicio);
    if (servicio =="Tipo de servicio"  && folio == ""){
        console.log("NADA DE INFO");
    }
    else{
        if (servicio == "Tipo de servicio") {
            // console.log("servicio inservible");

            servicio = null
        }
        getDocs(folio, servicio)
    }
})



var url = 'http://localhost:8000/documentos/search_docs/'
function getDocs(folio,tpServicio, rutCli = null ) {
    // const HTMLResponse = document.querySelector("#tablaJS")
    const tbody = document.querySelector("#tablaJS")
    const tr = document.createElement("tr")
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
        response.json().then(docs => {
            let body = '';
            let clase = "centrado",
                cssButton = "buttonDownload";
            docs.map((doc) => {
                let button = `<button class="${cssButton}">Procesar</button>`
                let tdfolio = `<td class = "${clase}">${doc.folio}</td>`,
                    tdnomDoc = `<td class = "${clase}">${doc.nomDoc}</td>`,
                    tdRutReceptor = `<td class = "${clase}">${doc.rut_receptor}</td>`,
                    tdTpServicio = `<td class = "${clase}">${doc.tipo_servicio}</td>`,
                    tdProcesar = `<td class = "${clase}" id ="#procesar">${button}</td>`;

                body += `<tr>${tdfolio}${tdnomDoc}${tdRutReceptor}${tdTpServicio}${tdProcesar}</tr>`;
                tbody.innerHTML += body;
    
            });
 
        })
    });
}
