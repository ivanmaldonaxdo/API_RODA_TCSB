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

function getClient() {
    const url = "http://3.239.229.60/clientes/"+user
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
            document.getElementById("nom").value=data.nom_cli
            document.getElementById("rut").value=data.rut_cliente
            document.getElementById("razon").value=data.razon_social
        })
    });
}

getClient()


document.querySelector('form.form-cont').addEventListener('submit', function (e) {
    e.preventDefault()
    var nom_cli = document.getElementById('nom');
    var rut_cli = document.getElementById('rut');
    var razon_cli = document.getElementById('razon');
    modifyClient(nom_cli.value, rut_cli.value, razon_cli.value)
});


function modifyClient(nom_cli, rut_cli, razon_cli) {
    const url = 'http://3.239.229.60/clientes/'+user+'/'
    console.log(url)
    console.log(nom_cli, rut_cli, razon_cli)
    fetch(url, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({ 
            'nom_cli': nom_cli,
            'rut_cliente': rut_cli,
            'razon_social': razon_cli,
        })

    })
    .then((response) => {
        response.json().then(data => {
            if (response.status == 200) {
                Swal.fire({
                    title:'Cliente Actualizado Correctamente',
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