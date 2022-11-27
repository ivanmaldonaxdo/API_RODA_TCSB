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




document.querySelector('form.form-cont').addEventListener('submit', function (e) {

    //prevent the normal submission of the form
    e.preventDefault();
    var correo = document.getElementById('emailuser');
    var password = document.getElementById('passuser');
    var nombre = document.getElementById('nomuser');
    var telefono = document.getElementById('celuser');
    var rol = document.getElementById('rol');
    createUser(correo.value, password.value, nombre.value, telefono.value, rol.value)
});

function createUser(correo, password, nombre, telefono, rol) {
    const url = 'http://localhost:8000/usuarios/'
    console.log(correo, password, nombre, telefono, rol)
    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({ 
            'email': correo,
            'password': password,
            'name': nombre,
            'telefono':telefono,
            'role':rol 
        })
        
    })

    .then((response) => {
        
        response.json().then(data => {
            if (response.status == 201) {
                Swal.fire({
                    title:'Usuario Registrado Correctamente',
                    icon:'success',
                    
                })
            }
            else {
                
                Swal.fire({
                    title:data['message'],
                    icon:'error',
                    text:Object.values(data['errors'])[0],
                })
            }

        })
    });
}