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
    var nom_cli = document.getElementById('nom_cli');
    var rut_cli = document.getElementById('rut_cli');
    var razon = document.getElementById('razon');
    createClient(nom_cli.value, rut_cli.value, razon.value)
});

function createClient(nom_cli, rut_cli, razon) {
    const url = 'http://3.239.33.153/clientes/'
    console.log(nom_cli, rut_cli, razon)
    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({ 
            'nom_cli': nom_cli,
            'rut_cliente': rut_cli,
            'razon_social': razon,
        })
        
    })

    .then((response) => {
        
        response.json().then(data => {
            if (response.status == 201) {
                Swal.fire({
                    title:'Cliente Registrado Correctamente',
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