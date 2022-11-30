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

usuario = document.getElementsByClassName("usuario")

proce = document.getElementsByClassName("proce")

cron = document.getElementsByClassName("cronn")
log = document.getElementsByClassName("logg")
suc = document.getElementsByClassName("suc")

function rol(){
    const url = 'http://3.239.33.153/rol_usuario/'
    fetch(url, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
       

    })
    .then(response => response.json())
    .then(data=>{
        console.log(data.Rol)
        
        if(data.Rol==3){    
            $(usuario).hide()
            $(proce).hide()
            $(cron).hide()
            $(log).hide()
            $(suc).hide()
            console.log("usuario");
        }else if(data.Rol==2){
            $(usuario).hide()
            $(suc).hide()
            $(proce).show()
            $(cron).show()
            console.log("operador");

        }
        
    })
    .catch(err=>console.log(err))
}
var roles = rol();