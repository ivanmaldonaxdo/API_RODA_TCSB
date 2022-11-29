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

document.querySelector('form.crondata').addEventListener('submit', function(e) {

    //prevent the normal submission of the form
    e.preventDefault();
    var hora = document.getElementById("horacron");
    var fecha = document.getElementById("fechacron");
    var estado = document.getElementById("estado");
    var status
    if (estado.value == false) {
        status = false
    } else {
        status = true
    }
    actCron(hora.value, fecha.value, status)

});

function actCron(hora, fecha, estado) {
    const url = "http://localhost:8000/cron/actualizar_parametros_cron/"
    fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken,
            },
            body: JSON.stringify({
                "hora_exec": hora,
                "fecha": fecha,
                "is_active": estado
            })

        })
        .then((response) => {
            response.json().then(data => {
                if (response.status == 200) {
                    Swal.fire({
                        title: 'Parametros Actualizados',
                        icon: 'success',
                    }).then(() => location.reload())
                } else {
                    Swal.fire({
                        title: 'Error en la actualizacion',
                        icon: 'error',
                    })
                }

            })
        });
}

function getCron() {
    const url = "http://localhost:8000/cron/info_cron/"
    fetch(url, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken,
            },

        })
        .then((response) => {
            response.json().then(data => {
                Object.entries(data).forEach(([key, value]) => {
                    document.getElementById("infoCron").value += '  ' + key + ': ' + value + "\n"


                });
            })
        });

}

function getcronparams() {
    const url = "http://localhost:8000/cron/get_cron_params/"
    fetch(url, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken,
            },

        })
        .then((response) => {
            response.json().then(data => {
                document.getElementById('fechacron').value = data['fecha']
                document.getElementById('horacron').value = data['hora_exec']
                document.getElementById('estado').value = data['is_active']
            })
        });
}
getcronparams()
getCron();