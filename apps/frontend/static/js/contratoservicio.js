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
    var num_cli = document.getElementById('cli');
    var sucu = document.getElementById('sucu');
    var prov = document.getElementById('prov');
    createContract(num_cli.value, sucu.value, prov.value)
});

function createContract(num_cli, sucu, prov) {
    const url = 'http://3.239.229.60/sucursales/contratos/create_contract/'
    console.log(num_cli, sucu, prov)
    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({ 
            'num_cliente': num_cli,
            'sucursal': sucu,
            'proveedor': prov,
        })
        
    })

    .then((response) => {
        
        response.json().then(data => {
            if (response.status == 201) {
                Swal.fire({
                    title:'Contrato Registrado Correctamente',
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