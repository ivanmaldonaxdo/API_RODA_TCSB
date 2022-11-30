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

let user = localStorage.getItem('Idcliente')

function getContract() {
    const url = "http://100.26.4.115/sucursales/contratos/create_contract/"+user
    fetch(url, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },

    })
    .then((response) => {
        response.json().then(data => {
            console.log(data)
            document.getElementById("cli").value=data.num_cliente
            document.getElementById("sucu").value=data.sucursal
            document.getElementById("prov").value=data.proveedor
        })
    });
}

getContract()

document.querySelector('form.form-cont').addEventListener('submit', function (e) {

    //prevent the normal submission of the form
    e.preventDefault();
    var num_cli = document.getElementById('cli');
    var sucu = document.getElementById('sucu');
    var prov = document.getElementById('prov');
    createContract(num_cli.value, sucu.value, prov.value)
});

function modifyContract(num_cli, sucu, prov) {
    const url = 'http://100.26.4.115/sucursales/contratos/create_contract/'+user+'/'
    console.log(url)
    console.log(nom_cli, rut_cli, razon_cli)
    fetch(url, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({ 
            'nom_cli': num_cli,
            'rut_cliente': sucu,
            'razon_social': prov,
        })

    })
    .then((response) => {
        response.json().then(data => {
            if (response.status == 200) {
                Swal.fire({
                    title:'Contrato Actualizado Correctamente',
                    icon:'success',
                    
                }).then(function(){
                    location.reload();
                })
            }
            else {
                Swal.fire({
                    title:'Error en la actualizacion',
                    icon:'error',
                })
            }
        })
    });
}