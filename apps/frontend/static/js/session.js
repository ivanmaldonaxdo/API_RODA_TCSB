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
    logoutUser()
})

// var url = 'http://52.201.38.209/auth-user/'

function logoutUser(){
    const url = 'http://localhost:8000/logout/'
    fetch(url,{
    method:'GET',
    headers:{
        'Content-Type':'application/json',
        'X-CSRFToken': csrftoken,
    },

})
.then((response) => {response.json().then(data => {                  
if(response.ok){         
    window.location.replace("http://localhost:8000/front/");
    } 
else{
    console.log(response.data)
    }
})});
}
