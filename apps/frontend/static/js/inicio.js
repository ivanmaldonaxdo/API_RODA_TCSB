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
            // let sucur_select = document.querySelector('#sucursal');
            response.json().then(sucursales => {
                // console.log(Array.from(sucursales).length);
                document.getElementById("totalSucur").textContent = Array.from(sucursales).length;
                // Array.from(sucursales).length()
                Array.from(sucursales).map(sucur => 
                    {
                        createRowSucur(sucur);
                        // let newOption = new Option(s.nom_sucursal,s.id);
                        // sucur_select.add(newOption,undefined);
                        // console.log(s.id);
                    }                    
                )
            })
        }
     });
}



function createRowSucur(sucur) 
{
    const tbody = document.querySelector("#tbodySucursales");
    let body = '';
    // let clase = "centrado",
    //     cssButton = "buttonDownload";
    let clase = "centrado";
    let tdDireccion = `<td class = "${clase}" data-label="Direccion">${sucur.direccion}</td>`,
        tdSucur = `<td class = "${clase}"  data-label="Nombre sucursal">${sucur.nom_sucursal}</td>`,
        tdComuna = `<td class = "${clase}" data-label="Comuna">${sucur.comuna}</td>`,
        tdCliente = `<td class = "${clase}" data-label="Cliente">${sucur.cliente}</td>`;
        // tdDownload = `<td class = "${clase}" data-label="Documento">${hrefDownload} </td>`;


        // "comuna": 109,
        // "cliente": 1
    body += `<tr">${tdSucur}${tdDireccion}${tdComuna}${tdCliente}</tr>`;
    tbody.innerHTML += body;
    
}

setSucursales();