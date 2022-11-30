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

document.getElementById('cerrarsession').addEventListener('click', function(){
    Swal.fire({
        title: '¿Cerrar Sesión?',
        type: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#3085d6',
        cancelButtonColor: '#d33',
        confirmButtonText: 'OK',
        closeOnConfirm: true,
        closeOnCancel: true
    }).then((result) => {
        if (result.value==true){
            logoutUser()
        }
    })
})

// var url = 'http://52.201.38.209/auth-user/'

function logoutUser(){
    // const url = 'http://3.80.228.126/logout/'
    const url = 'http://3.239.229.60/logout/'

    fetch(url,{
    method:'GET',
    headers:{
        'Content-Type':'application/json',
        'X-CSRFToken': csrftoken,
    },
    })
    .then((response) => {response.json().then(data => {                  
    if(response.ok){         
        Swal.fire({
            title: "Sesion cerrada correctamente"
        }).then(() => {
            window.location.replace("http://3.239.229.60/");
        })
        } 
    else{
        console.log(response.data)
        }
    })});
    }
