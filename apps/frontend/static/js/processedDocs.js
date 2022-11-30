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

function setSucursales() {
    const url = new URL("http://3.219.56.115/sucursales/");
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
        if (status_code >= 400 ){
            console.log( response.json().catch(err => console.error(err)));
        }
        else {
            // console.log(response.json());
            // let newOption = new Option('Option Text','Option Value');
            let sucur_select = document.querySelector('#sucursal');
           
            // sucur_select.add(newOption,undefined);
            // console.log(sucur_select);
            response.json().then(sucursales => {
                Array.from(sucursales).map(s => 
                    {
                        let newOption = new Option(s.nom_sucursal,s.id);
                        sucur_select.add(newOption,undefined);
                        console.log(s.id);
                    }                    
                )
                
            })
            
        }
     });
}
// setSucursales();

async function setDataSucur(idCli) {
    const url = new URL("http://3.219.56.115/sucursales/");
    const params = {cliente :idCli }
    url.search = new URLSearchParams(params).toString();
    const res = await fetch(url, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        }
    })
    obj = await res.json();
    return obj
}




async function setDataClientes() {
    const url = new URL("http://3.219.56.115/clientes/");
    const res = await fetch(url, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        }
    })
    obj = await res.json();
    return obj
}


setDataClientes().then(clientes => {
    let clientes_select = document.querySelector('#clientes');
    Array.from(clientes).map(cli => 
        {
            let newOption = new Option(cli.nom_cli,cli.id);
            clientes_select.add(newOption,undefined);
            // console.log(s.id);
        }                    
    )    
})


document.getElementById('clientes').addEventListener("change",function (e) {
    e.preventDefault();
    e.stopImmediatePropagation();
    let cli_selected = document.getElementById('clientes').value;
    console.log(cli_selected);

    setDataSucur(cli_selected).then(sucursales => {
        let sucur_select = document.querySelector('#sucursal');
        let index = document.getElementById('clientes').selectedIndex;


        if (index == 0) {
                // console.log(s.id);
            sucur_select.innerHTML = '';
            let newOption = new Option('Sucursal...','');
            sucur_select.add(newOption,undefined);
        }
        else{
            sucur_select.innerHTML = '';
            Array.from(sucursales).map(s => 
                {
                    let newOption = new Option(s.cod, s.id);
                    sucur_select.add(newOption,undefined);
                    // console.log(s.id);
                }                    
            )
         
        }
     
        
    })


    
})
/////////////////////////BUSQUEDA DE DOCUMENTOS
document.getElementById("buscarDocs").addEventListener('click', function (e) {
    let sucursal = document.getElementById('sucursal').value,
        cliente = document.getElementById('clientes').value
        folio = document.getElementById('folio').value,
        fecha = document.querySelector('#fecha').value,
        rut_emisor = document.getElementById("rut").value;
    // fecha = String(fecha);
    console.log(fecha);
    // console.log(sucursal);
    // console.log(sucursal ?? null);
    // console.log(cliente ?? null);
    // console.log('XD ' ,num_cliente,' XD');
    const paramsSearch =  { 
        contrato_servicio__sucursal: sucursal,
        contrato_servicio__sucursal__cliente:cliente,
        search : folio,
        fecha_procesado__date:fecha,
        contrato_servicio__proveedor__rut_proveedor :rut_emisor

        }
    
    Swal.fire({
        title: 'Buscando documentos procesados....',
        timerProgressBar: true,
        didOpen: () => {
            Swal.showLoading()
            // getProcesedDocs();
            console.log(paramsSearch);
            getProcesedDocs(paramsSearch);
            // getProcesedDocs();


        },
  
    })
    e.preventDefault();
    e.stopImmediatePropagation();

})

function getProcesedDocs(paramsURL) {
    const url = new URL("http://3.219.56.115/procesados/");
    // const params = { contrato_servicio: rutProveedor }
    const params = paramsURL;
    url.search = new URLSearchParams(params).toString();
    console.log(url.search);

    // const url = 'http://3.80.228.126/procesados/
    // const url = 'http://3.219.56.115/procesados/';
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
    var urlBase = 'http://3.219.56.115';
    //server
    // var urlBase = 'http://localhost'
    var urlDownload = urlBase + doc.documento

    let btnDownload = `<button id = "downloadDoc" class="${cssButton}" type="button"> Descargar</button>`;
    let hrefDownload = `<a href = "${urlDownload}" download> ${btnDownload}</a>`;

    let tdfolio = `<td class = "${clase}" data-label="Folio">${doc.folio}</td>`,
        tdSucur = `<td class = "${clase}"  data-label="Sucursal">${doc.rut_sucursal}</td>`,
        tdFechaProcess = `<td class = "${clase}" data-label="Fecha Procesado">${doc.fecha}</td>`,
        tdDownload = `<td class = "${clase}" data-label="Documento">${hrefDownload} </td>`;



    body += `<tr">${tdfolio}${tdFechaProcess}${tdDownload}</tr>`;
    tbody.innerHTML += body;
    
}
function clearTable(){
    const table = document.querySelector("#tbodyProcessed");
    table.innerHTML = '';
}

function pasarIdCli(idCli) {
    $.ajax({
        type: "GET",
        url: '/get_client',
        data: {
            "id_cli": idCli,
        },
        dataType: "json",
        success: function (data) {
            console.log(data);
            // any process in data
            // alert("successfull")
        },
        failure: function () {
            console.log("fallo");
            // alert("failure");
        }
    });
    
}
//referencias js
//https://stackoverflow.com/questions/68933909/how-to-pass-hidden-field-in-table-and-return-the-value-in-jquery-on-tr-click
//https://bobbyhadz.com/blog/javascript-map-is-not-a-function#:~:text=The%20"TypeError%3A%20map%20is%20not,of%20how%20the%20error%20occurs.

