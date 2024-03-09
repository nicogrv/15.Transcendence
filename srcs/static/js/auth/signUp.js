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
document.getElementById('signUpForm').addEventListener('submit', function(e) {
    e.preventDefault();
    var name = document.getElementById('signUpUsername').value;
    var email = document.getElementById('signUpEmail').value;
    var password = document.getElementById('signUpPassword').value;
    var confirmPassword = document.getElementById('signUpConfirmPassword').value;
    if (name === '') 
        return createAlerte('Name is required', 5000);
    else if (email === '') 
        return createAlerte('email is required', 5000);
    else if (password === '') 
        return createAlerte('password is required', 5000);
    else if (confirmPassword === '') 
        return createAlerte('confirmPassword is required', 5000);
    else if (password != confirmPassword) 
        return createAlerte('Password and confirm password are not shown', 5000);
    else
        return createAlerte('coucou', 5000);

    });