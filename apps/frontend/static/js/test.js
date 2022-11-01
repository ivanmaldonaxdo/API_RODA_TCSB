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
////////

let folio = 11419589
let tpServicio = null
let rut = null
document.getElementById("get-users").addEventListener('click', function(e){
    getUser()
    })



    var url = 'http://localhost:8000/documentos/search_docs/'
    function getUser(){
        fetch(url,{
            method:'POST',
            headers:{
            'Content-Type':'application/json',
            'X-CSRFToken': csrftoken,
        },
        body:JSON.stringify({
                         "folio":folio,
                         "tipo_servicio":tpServicio,
                         "rut_receptor":rut
                     })

    })
    .then((response) => {response.json().then(data => {    
        console.log(data)
    })});
    }