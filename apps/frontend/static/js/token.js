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
var loginForm = document.getElementById('login')
loginForm.addEventListener('submit', function (e) {
    e.preventDefault()
})

document.getElementById('btnLogin').addEventListener('click', function (e) {
    loginUser()
})

function loginUser() {
    // const url = 'http://3.80.228.126/auth-user/'
    const url = 'http://3.239.229.60/auth-user/'
    const inicio = "http://3.239.229.60/inicio/"
    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({ 'email': login.email.value, 'password': login.password.value })

    })
    .then((response) => {
        response.json().then(data => {
            if (response.status == 202) {
                Swal.fire({
                    title:'Sesion iniciada correctamente',
                    icon:'success',
                }).then(function(){
                    window.location = inicio;
                })
            }
            else {
                Swal.fire({
                    title:data['message'],
                    icon:'error',
                   
                })
            }
        })
    });
}
