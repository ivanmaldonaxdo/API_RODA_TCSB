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


document.getElementById("get-users").addEventListener('click', function(e){
    getUser()
    })



    var url = 'http://localhost:8000/usuarios/'
    function getUser(){
        fetch(url,{
            //credentials: 'include',
            method:'GET',
            headers:{
            'Content-Type':'application/json',
            'X-CSRFToken': csrftoken,
        },
    })
    .then((response) => {response.json().then(data => {                  
        console.log(data)
    })});
    }