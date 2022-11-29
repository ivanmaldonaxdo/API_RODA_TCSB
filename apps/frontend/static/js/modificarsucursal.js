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


let user = localStorage.getItem('Idsucursal')

function getsucursal() {
    const url = "http://localhost:8000/sucursales/" + user
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
                document.getElementById("nom").value = data.nom_sucursal
                document.getElementById("codi").value = data.cod
                document.getElementById("direc").value = data.direccion
                document.getElementById("comuna").value = data.comuna
                document.getElementById("cliente").value = data.cliente
            })
        });
}

getsucursal()


document.querySelector('form.form-cont').addEventListener('submit', function(e) {
    e.preventDefault()
    var nom = document.getElementById('nom');
    var cod = document.getElementById('codi');
    var direccion = document.getElementById('direc');
    var comuna = document.getElementById('comuna');
    var cliente = document.getElementById('cliente');
    modifyUser(nom.value, cod.value, direccion.value, comuna.value, cliente.value)
});


function modifyUser(nom, cod, direccion, comuna, cliente) {
    const url = 'http://localhost:8000/sucursales/' + user + '/'
    console.log(url)
    console.log(nom, cod, direccion, comuna, cliente)
    fetch(url, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken,
            },
            body: JSON.stringify({

                'nom': nom,
                'cod': cod,
                'direccion': direccion,
                'comuna': comuna,
                'cliente': cliente
            })
        })
        .then((response) => {
            response.json().then(data => {
                if (response.status == 200) {
                    Swal.fire({
                        title: 'sucursal Actualizada Correctamente',
                        icon: 'success',
                    }).then(function() {
                        location.reload();
                    })
                } else {
                    Swal.fire({
                        title: 'Error en la actualizacion',
                        icon: 'error',
                    })
                }
            })
        });
}