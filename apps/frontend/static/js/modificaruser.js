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


let user = localStorage.getItem('idusuario')

function getUser() {
    const url = "http://100.27.17.66/usuarios/"+user
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
            document.getElementById("nom").value=data.name
            document.getElementById("email").value=data.email
            document.getElementById("tef").value=data.telefono
            document.getElementById("rol").value=data.role
        })
    });
}

getUser()


document.querySelector('form.form-cont').addEventListener('submit', function (e) {
    e.preventDefault()
    var correo = document.getElementById('email');
    var nombre = document.getElementById('nom');
    var telefono = document.getElementById('tef');
    var rol = document.getElementById('rol');
    modifyUser(correo.value, nombre.value, telefono.value, rol.value)
});


function modifyUser(correo, nombre, telefono, rol) {
    const url = 'http://100.27.17.66/usuarios/'+user+'/'
    console.log(url)
    console.log(correo, nombre, telefono, rol)
    fetch(url, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({ 
            'email': correo,
            'name': nombre,
            'telefono':telefono,
            'role':rol 
        })

    })
    .then((response) => {
        response.json().then(data => {
            if (response.status == 200) {
                Swal.fire({
                    title:'Usuario Actualizado Correctamente',
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
 