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
    const url = new URL("http://localhost:8000/sucursales/");
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
    const url = new URL("http://localhost:8000/sucursales/");
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
    const url = new URL("http://localhost:8000/clientes/");
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
    
    limpiaCBO();
    console.log(cli_selected);
    setDataSucur(cli_selected).then(sucursales => {
        let sucur_select = document.querySelector('#sucursal');
        // let index = document.getElementById('clientes').selectedIndex;
        Array.from(sucursales).map(s => 
            {
                let newOption = new Option(s.nom_sucursal,s.id);
                sucur_select.add(newOption,undefined);
                // console.log(s.id);
            }                    
        )
        // if (index > 0) {
        // }
    
})


    
})
let limpiaCBO = ()=>{
    let sucur_select = document.querySelector('#sucursal');  
   
    // while (sucur_select.options.length > 0) {
    //     sucur_select.remove(1);
    // }
    // if sucur_select.selec
    // for (let i = 1; i < sucur_select.options.length; i++) {
    //     selected.remove(i);
    //     // selected[i] = listbox.options[i].selected;
    // }
} 

// chainSucurCli();
////////
document.getElementById("buscarDocs").addEventListener('click', function (e) {
    let sucursal = document.getElementById('sucursal').value,
        cliente = document.getElementById('clientes').value;

    // console.log(sucursal ?? null);
    // console.log(cliente ?? null);
    // console.log('XD ' ,num_cliente,' XD');
    const paramsSearch =  { 
        contrato_servicio__sucursal: sucursal,
        contrato_servicio__sucursal__cliente:cliente
        }
    Swal.fire({
        title: 'Buscando documentos procesados....',
        timerProgressBar: true,
        didOpen: () => {
            Swal.showLoading()
            // getProcesedDocs();
            // getProcesedDocs(paramsSearch);
            getProcesedDocs();


        },
  
    })
    e.preventDefault();
    e.stopImmediatePropagation();

})

function getProcesedDocs(paramsURL) {
    const url = new URL("http://localhost:8000/procesados/");
    // const params = { contrato_servicio: rutProveedor }
    // const params = paramsURL;
    // url.search = new URLSearchParams(params).toString();

    // const url = 'http://3.80.228.126/procesados/
    // const url = 'http://localhost:8000/procesados/';
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
                // docs = new Array.isArray(docs) ? docs.sort((a,b)=>{
                //     return new Date(b.fecha) - new Date(a.fecha);
                // }) : docs;
                // docs = new Array(docs).sort((a,b)=>{
                //     return new Date(b.fecha) - new Date(a.fecha);
                // }).reverse().map(e=> console.log(e))
                // // docs = new Map(docs).a
                
                /////String(a[1]).localeCompare(b[1])
                // docs = Array.isArray(docs) ? docs.sort((a,b) =>a.fecha.localcompare(b.fecha)) : docs;
                
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

//referencias js
//https://stackoverflow.com/questions/68933909/how-to-pass-hidden-field-in-table-and-return-the-value-in-jquery-on-tr-click
//https://bobbyhadz.com/blog/javascript-map-is-not-a-function#:~:text=The%20"TypeError%3A%20map%20is%20not,of%20how%20the%20error%20occurs.
