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
    console.log(folio);
    console.log(servicio);
    if (servicio =="Tipo de servicio"  && folio == ""){
        console.log("NADA DE INFO");
    }
    else{
        if (servicio == "Tipo de servicio") {
            // console.log("servicio inservible");

            servicio = null;
        }
        getDocs(folio, servicio);
    }
    e.preventDefault();
    e.stopImmediatePropagation();

})


// let tbody_respaldo = "" 
var url = 'http://localhost:8000/documentos/search_docs/'
function getDocs(folio,tpServicio, rutCli = null ) {
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
        response.json().then(docs => {
            // let cantidad = Object.keys(docs).length 
            // if ( typeof(docs) == "object") {
            //     createRowDoc(docs);
            // } else if ( typeof(docs) == "list"){
            //     docs.map((doc) => {
            //         createRowDoc(doc);
            //     });
            // }
            Array.isArray(docs) ? docs.map(doc =>  createRowDoc(doc)) : createRowDoc(docs);

            // docs.forEach(doc => {
            //     createRowDoc(doc);
            // });
            // docs.map((doc) => {
            //     createRowDoc(doc);
            // });
        })
    });

}

function clickStopper(event) {
    event.stopPropagation();
    return;
}
//onclick="myFunction(this)"
// function myFunction()
function getIndexTR(x) {
    let index_tb = x.rowIndex;
    let conteo_celdas_filas = document.getElementById("tablaJS").firstElementChild.childElementCount,
        elemento = document.getElementById("tablaJS").firstElementChild;
    let items_tr = x.cells[conteo_celdas_filas-1];
    // console.log(items_tr[3]);
    let uuid = document.getElementsByName("uuid").item(index_tb).value,
        nomDoc = document.getElementsByName("nomDoc").item(index_tb).value,
        RutEmi = document.getElementsByName("RutEmi").item(index_tb).value;
    console.log("uuid: ", uuid ," - nomDoc: ", nomDoc, " - RutEmi: ",RutEmi) ;


    // console.log("Elemento: ",elemento, " - Cantidad de celdas: ",conteo_celdas_filas);

    // "uuid"  
    // "nomDoc"
    // "RutEmi"


}


// function downloadDocs(x){
    
//         console.log(x.rowIndex);
//         // let data = document.getElementById("process-doc");
//         // console.log("Data del item seleccionado es =>", data );
    

        
// }  
    // let valores = x.value
    // let tabla = document.querySelector("table tbody").value;
    // console.log(tabla);
    // console.log(x.value);

    // document.addEventListener('click',function (params) {

    // })



    // if (btn_procesar) {
    //     btn_procesar.addEventListener('click', function (event) {
    //       btn_procesar.value
    //     })
    // }

function createRowDoc(doc,event) 
{
    const tbody = document.querySelector("#tablaJS");
    const data_btn = {uuid : doc.uuid, nomDoc : doc.nomDoc, rut_emisor: doc.rut_emisor};
    console.log(data_btn);    
    let body = '';
    let clase = "centrado",
        cssButton = "buttonDownload";
    // let data_value = doc.uuid + " | " + doc.nomDoc + " | " + doc.rut_emisor
    // console.log(data_value);
    let btn_uuid   = `<input type="hidden" id = "uuid"   name="uuid" value="${doc.uuid}"/>`,
        btn_nomDoc = `<input type="hidden" id = "nomDoc" name="nomDoc" value="${doc.nomDoc}"/>`,
        btn_RutEmi = `<input type="hidden" id = "RutEmi" name="RutEmi" value="${doc.rut_emisor}"/>`;
    let button = `<button id = 'process-doc' class="${cssButton}" type = 'button'  value = "" >Procesar</button>`;
    // let button = `<button id = 'process-doc' class="${cssButton}" type = 'button'  value = "${data_value} " onclick ="downloadDocs(this)">Procesar</button>`;
    let form_procesar = `<form action="">${btn_uuid}${btn_nomDoc}${btn_RutEmi}${button}</form>`;
    let tdfolio = `<td class = "${clase}">${doc.folio}</td>`,
        tdnomDoc = `<td class = "${clase}">${doc.nomDoc}</td>`,
        tdRutReceptor = `<td class = "${clase}">${doc.rut_receptor}</td>`,
        tdTpServicio = `<td class = "${clase}">${doc.tipo_servicio}</td>`,
        tdProcesar = `<td class = "${clase}">${form_procesar}</td>`;

    body += `<tr onclick = "getIndexTR(this)">${tdfolio}${tdnomDoc}${tdRutReceptor}${tdTpServicio}${tdProcesar}</tr>`;
    tbody.innerHTML += body;
    
}



//referencias js
//https://stackoverflow.com/questions/68933909/how-to-pass-hidden-field-in-table-and-return-the-value-in-jquery-on-tr-click
//https://bobbyhadz.com/blog/javascript-map-is-not-a-function#:~:text=The%20"TypeError%3A%20map%20is%20not,of%20how%20the%20error%20occurs.