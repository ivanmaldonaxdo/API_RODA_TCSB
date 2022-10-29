function makeRequest() {
    let headers = {}
    if (sessionStorage.token) {
        headers = { 'Authorization': sessionStorage.token }
    }
    fetch("/api/echo", { headers: headers })
        .then((res) => {
            if (res.status == 200) {
                return res.text()
            } else {
                throw Error(res.statusText)
            }
        }).then(responseText => logResponse("requestResponse", responseText))
        .catch(console.error)
    }