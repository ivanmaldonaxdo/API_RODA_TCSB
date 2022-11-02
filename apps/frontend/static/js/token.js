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
var loginForm = document.getElementById('login')
loginForm.addEventListener('submit', function(e){
    e.preventDefault()
    console.log('form enviado')
})

document.getElementById('btnLogin').addEventListener('click', function(e){
loginUser()
})

var url = 'http://3.89.164.205/auth-user/'
function loginUser(){
    fetch(url,{
    method:'POST',
    headers:{
        'Content-Type':'application/json',
        'X-CSRFToken': csrftoken,
    },
    body:JSON.stringify({'email':login.email.value, 'password': login.password.value})

})
.then((response) => {response.json().then(data => {                  
if(response.ok){         
    window.location.replace("http://3.89.164.205/inicio/");
    } 
else{
    console.log(response.data)
    }
})});
}