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
    var nom_dis = document.getElementById('nom_dis');
    var rut_prov = document.getElementById('rut_prov');
    var contacto = document.getElementById('contacto');
    var serv = document.getElementById('serv');
    createProv(nom_dis.value, rut_prov.value, contacto.value, serv.value)
});

function createProv(nom_dis, rut_prov, contacto, serv) {
    const url = 'http://100.27.17.66/proveedores/'
    console.log(nom_dis, rut_prov, contacto, serv)
    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({ 
            'nom_proveedor': nom_dis,
            'rut_proveedor': rut_prov,
            'contacto': contacto,
            'servicio': serv,
        })
        
    })

    .then((response) => {
        
        response.json().then(data => {
            if (response.status == 201) {
                Swal.fire({
                    title:'Proveedor Registrado Correctamente',
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