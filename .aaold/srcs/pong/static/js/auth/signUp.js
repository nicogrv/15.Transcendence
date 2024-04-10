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





const signUpForm = document.getElementById("signUpForm")
console.log(signUpForm)
signUpForm.addEventListener('submit', function(e) {
    e.preventDefault();
    var username = document.getElementById('signUpUsername').value;
    var email = document.getElementById('signUpEmail').value;
    var password = document.getElementById('signUpPassword').value;
    var confirmPassword = document.getElementById('signUpConfirmPassword').value;
    if (username === '') 
        return createAlerte('Username is required', 5000);
    else if (email === '') 
        return createAlerte('Email is required', 5000);
    else if (password === '') 
        return createAlerte('Password is required', 5000);
    else if (confirmPassword === '') 
        return createAlerte('ConfirmPassword is required', 5000);
    else if (password != confirmPassword) 
        return createAlerte('Password and confirm password are not shown', 5000);
    else {
         fetch(`${window.location.origin}/api/auth/signUp/?username=${username}&email=${email}&password=${password}`)
        .then(response => {
            if (!response.ok) {createAlerte('La requête a échoué');}return response.json(); })
        .then(data => {
            if ("error" in data)
                createAlerte(data.error, 5000)
            else {
                console.log("reload");
                location.href = `/`
            }
        })
    }
    });