function createAlerte(message, timeDeleteAlerte) {
    var alertDiv = document.createElement('div');
    alertDiv.className = 'alert alert-danger';
    alertDiv.setAttribute('role', 'alert');
    var alertText = document.createTextNode(message);
    alertDiv.appendChild(alertText);
    document.body.appendChild(alertDiv);
    setTimeout(function() {
        alertDiv.parentNode.removeChild(alertDiv);
    }, timeDeleteAlerte);
}


const signInForm = document.getElementById("signInForm")
signInForm.addEventListener('submit', function(e) {
    console.log("commmit");
    e.preventDefault();
    var username = document.getElementById('signInUsername').value;
    var password = document.getElementById('signInPassword').value;
    if (username === '') 
        return createAlerte('Username is required', 5000);
    else if (password === '') 
        return createAlerte('password is required', 5000);
    console.log("fetch");
    fetch(`http://127.0.0.1:8000/api/auth/signIn/?username=${username}&password=${password}`)
    .then(response => {
        if (!response.ok) {createAlerte('La requête a échoué');}return response.json(); })
    .then(data => {
        if ("error" in data)
            createAlerte(data.error, 5000)
        else
            location.href = `/`
    })
})
