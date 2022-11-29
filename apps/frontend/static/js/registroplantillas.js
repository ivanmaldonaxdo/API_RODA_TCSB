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


//id
//nom_doc
//queries_config
//tablas_config
//fecha_creacion
//proveedor

document.querySelector('form.form-cont').addEventListener('submit', function(e) {
    e.preventDefault();
    var id = document.getElementById('id');
    var nom_doc = document.getElementById('nom_doc');
    var queries_config = document.getElementById('queries_config');
    var fecha_creacion = document.getElementById('#fecha_creacion');
    var proveedor = document.getElementById('proveedor');
    createsucursal(id.value, nom_doc.value, queries_config.value, fecha_creacion.value, proveedor.value)
});

function createsucursal(id, nom_doc, queries_config, fecha_creacion, proveedor) {
    const url = 'http://localhost:8000/plantillas/'
    console.log(id, nom_doc, queries_config, fecha_creacion, proveedor)
    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({
            'id': id,
            'nom_doc': nom_doc,
            'queries_config': queries_config,
            'fecha_creacion': fecha_creacion,
            'proveedor': proveedor

        })

    })

    .then((response) => {

        response.json().then(data => {
            if (response.status == 201) {
                Swal.fire({
                    title: 'Plantilla registrada Correctamente',
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