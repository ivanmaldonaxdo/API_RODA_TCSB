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


let user = localStorage.getItem('Idplantilla')

function getplantilla() {
    const url = "http://localhost:8000/plantillas/" + user
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
                document.getElementById("nom_doc").value = data.nom_doc
                document.getElementById("fecha_creacion").value = data.fecha_creacion
                document.getElementById("proveedor").value = data.proveedor
                    //document.getElementById("queries_config").value = data.queries_config
                    //document.getElementById("tablas_config").value = data.tablas_config
            })
        });
}

getplantilla()


document.querySelector('form.form-cont').addEventListener('submit', function(e) {
    e.preventDefault()
    var nom_doc = document.getElementById('nom_doc');
    var fecha_creacion = document.getElementById('fecha_creacion');
    var proveedor = document.getElementById('proveedor');
    //var tablas_config = document.getElementById('tablas_config');
    //var queries_config = document.getElementById('queries_config');  tablas_config.value, queries_config.value
    modifyplantilla(nom_doc.value, fecha_creacion.value, proveedor.value, )
});

// , tablas_config, queries_config
function modifyplantilla(nom_doc, fecha_creacion, proveedor) {
    const url = 'http://localhost:8000/plantillas/' + user + '/'
    console.log(url)
    console.log(nom_doc, fecha_creacion, proveedor)
    fetch(url, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken,
            },
            body: JSON.stringify({
                'nom_doc': nom_doc,
                'fecha_creacion': fecha_creacion,
                'proveedor': proveedor
                    //'tablas_config': tablas_config,
                    //'queries_config': queries_config
            })
        })
        .then((response) => {
            response.json().then(data => {
                if (response.status == 200) {
                    Swal.fire({
                        title: 'plantilla Actualizada Correctamente',
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