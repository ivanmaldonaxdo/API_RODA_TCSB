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

var RegForm = document.getElementById("form-cliente" )
RegForm.addEventListener('submit', function (e) {
    e.preventDefault()
    console.log('form enviado')
})

document.getElementById("btn-registrar").addEventListener('click', function(e){
    RegisterUser()
})

function RegisterUser() {
    // const url = 'http://3.80.228.126/auth-user/'
    const url = 'http://44.197.147.109/usuarios/'
    formulario = {
        'email' : RegForm.email.value,
        'password': RegForm.password.value,
        'name': RegForm.nomuser.value,
        'telefono':RegForm.celuser.value,
         'role':RegForm.rol.value

    }



    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({ 'email': formulario.email, 'password': formulario.password, 'name':formulario.nomuser, 'telefono':formulario.celuser, 'role':formulario.rol })

    })
    .then((response) => {
        response.json().then(data => {
            if (response.status == 201) {
                window.alert(data)
            }
            else {
                console.log(data)
            }

        })
    });
}