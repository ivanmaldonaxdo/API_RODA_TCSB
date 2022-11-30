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



document.querySelector('form.form-cont').addEventListener('submit', function(e) {

    //prevent the normal submission of the form
    e.preventDefault();
    var id = document.getElementById('id');
    var nom_sucursal = document.getElementById('nom_sucursal');
    var cod = document.getElementById('cod');
    var direccion = document.getElementById('direccion');
    var comuna = document.getElementById('comuna');
    var cliente = document.getElementById('cliente');
    createsucursal(id.value, nom_sucursal.value, cod.value, direccion.value, comuna.value, cliente.value)
});

function createsucursal(id, nom_sucursal, cod, direccion, comuna, cliente) {
    const url = 'http://100.26.4.115/sucursales/'
    console.log(id, nom_sucursal, cod, direccion, comuna, cliente)
    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({

            'id': id,
            'nom_sucursal': nom_sucursal,
            'cod': cod,
            'direccion': direccion,
            'comuna': comuna,
            'cliente': cliente
        })

    })

    .then((response) => {

        response.json().then(data => {
            if (response.status == 201) {
                Swal.fire({
                    title: 'Sucursal registrada Correctamente',
                    icon: 'success',

                })
            } else {

                Swal.fire({
                    title: data['message'],
                    icon: 'error',
                    text: Object.values(data['errors'])[0],
                })
            }

        })
    });
}