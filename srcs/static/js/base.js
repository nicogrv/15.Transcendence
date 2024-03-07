function initLoginPage() {

    const divSignInUp42Flex = document.createElement('div');
    divSignInUp42Flex.classList.add('divSignInUp42-flex');
    
    const divSignInUp42 = document.createElement('div');
    divSignInUp42.classList.add('divSignInUp42');
    
    const formContainerGreen = document.createElement('div');
    formContainerGreen.classList.add('form-containerGreen');
    
    const formLogin = document.createElement('form');
    
    const h3Login = document.createElement('h3');
    h3Login.textContent = 'Login';
    h3Login.style.textAlign = 'center';
    
    const divlogin = document.createElement('div');
    divlogin.classList.add('mb-3');
    
    const labellogin = document.createElement('label');
    labellogin.setAttribute('for', 'exampleInputEmail1');
    labellogin.classList.add('form-label');
    labellogin.textContent = 'login';
    
    const inputlogin = document.createElement('input');
    inputlogin.setAttribute('type', 'email');
    inputlogin.classList.add('form-control');
    inputlogin.setAttribute('id', 'exampleInputEmail1');
    inputlogin.setAttribute('aria-describedby', 'emailHelp');
    
    const divPassword = document.createElement('div');
    divPassword.classList.add('mb-3');
    
    const labelPassword = document.createElement('label');
    labelPassword.setAttribute('for', 'exampleInputPassword1');
    labelPassword.classList.add('form-label');
    labelPassword.textContent = 'Password';
    
    const inputPassword = document.createElement('input');
    inputPassword.setAttribute('type', 'password');
    inputPassword.classList.add('form-control');
    inputPassword.setAttribute('id', 'exampleInputPassword1');
    
    const submitButton = document.createElement('button');
    submitButton.setAttribute('type', 'submit');
    submitButton.classList.add('btn-css', 'btn-GentleGreen');
    submitButton.textContent = 'Submit';
    
    const btnLog42 = document.createElement('div');
    btnLog42.classList.add('btnLog42');
    btnLog42.addEventListener("click", (e) => {
        location.href = ("https://api.intra.42.fr/oauth/authorize?client_id=u-s4t2ud-9198daa6a4877961ff5b7a3ca58e5990fd4f618ddc61420e8aa18e18ed316472&redirect_uri=http%3A%2F%2F127.0.0.1%3A8000%2F&response_type=code")
    })
    
    
    const btnSign42 = document.createElement('button');
    btnSign42.setAttribute('type', 'submit');
    btnSign42.classList.add('btn-css', 'btn-Log42');
    btnSign42.textContent = 'Sign with 42';
    
    divSignInUp42Flex.appendChild(divSignInUp42);
    divSignInUp42.appendChild(formContainerGreen);
    formContainerGreen.appendChild(formLogin);
    formLogin.appendChild(h3Login);
    formLogin.appendChild(divlogin);
    divlogin.appendChild(labellogin);
    divlogin.appendChild(inputlogin);
    formLogin.appendChild(divPassword);
    divPassword.appendChild(labelPassword);
    divPassword.appendChild(inputPassword);
    formLogin.appendChild(submitButton);
    divSignInUp42.appendChild(btnLog42);
    btnLog42.appendChild(btnSign42);
    
    const formContainerPink = document.createElement('div');
    formContainerPink.classList.add('form-containerPink');
    
    const formSignIn = document.createElement('form');
    
    const h3SignIn = document.createElement('h3');
    h3SignIn.textContent = 'Sign in';
    h3SignIn.style.textAlign = 'center';
    
    const divConfirmPassword = document.createElement('div');
    divConfirmPassword.classList.add('mb-3');
    
    const labelConfirmPassword = document.createElement('label');
    labelConfirmPassword.setAttribute('for', 'exampleInputPassword1');
    labelConfirmPassword.classList.add('form-label');
    labelConfirmPassword.textContent = 'Confirm Password';
    
    const inputConfirmPassword = document.createElement('input');
    inputConfirmPassword.setAttribute('type', 'password');
    inputConfirmPassword.classList.add('form-control');
    inputConfirmPassword.setAttribute('id', 'exampleInputPassword1');
    
    
    const submitButtonPink = document.createElement('button');
    submitButtonPink.setAttribute('type', 'submit');
    submitButtonPink.classList.add('btn-css', 'btn-GentlePink');
    submitButtonPink.textContent = 'Submit';
    
    divSignInUp42Flex.appendChild(formContainerPink);
    formContainerPink.appendChild(formSignIn);
    formSignIn.appendChild(h3SignIn);
    formSignIn.appendChild(divlogin.cloneNode(true)); 
    formSignIn.appendChild(divPassword.cloneNode(true)); 
    formSignIn.appendChild(divConfirmPassword);
    divConfirmPassword.appendChild(labelConfirmPassword);
    divConfirmPassword.appendChild(inputConfirmPassword);
    formSignIn.appendChild(submitButtonPink);
    document.body.appendChild(divSignInUp42Flex);
    
}

function getParameterValue(parameterName) {
    var queryString = window.location.search;
    queryString = queryString.substring(1);
    var parameters = queryString.split("&");
    for (var i = 0; i < parameters.length; i++) {
        var parameter = parameters[i].split("=");
        if (parameter[0] === parameterName) {
            return decodeURIComponent(parameter[1]);
        }
    }
    return null;
}



function getCookie(cookieName) {
    var cookies = document.cookie.split(';');
    for(var i = 0; i < cookies.length; i++) {
        var cookie = cookies[i];
        cookie = cookie.trim();
        if(cookie.indexOf(cookieName + '=') === 0) {
            return cookie.substring(cookieName.length + 1);
        }
    }
    return null;
}

function createAlerte(message, timeDeleteAlerte) {
    var alertDiv = document.createElement('div');
    alertDiv.className = 'alert alert-danger';
    alertDiv.setAttribute('role', 'alert');
    var alertText = document.createTextNode(message);
    alertDiv.appendChild(alertText);
    document.body.appendChild(alertDiv);
    setTimeout(function() {
        alertDiv.parentNode.removeChild(alertDiv);
    }, 5000);
}

var token = getCookie('PongToken')
var messageQuery = getParameterValue('message')
queryValueCode = getParameterValue("code")

console.log("Token récupéré : ", token);
console.log("queryValueCode: ", queryValueCode)
if (messageQuery)
{
    initLoginPage()
    createAlerte(messageQuery, 5000)
}
else if (queryValueCode && !token) {
    fetch(`http://127.0.0.1:8000/api/auth/authWithFortyTwo?code=${queryValueCode}`)
    .then(response => {
        if (!response.ok) {throw new Error('La requête a échoué');}return response.json(); })
    .then(data => {
        console.log(data);
        if ('error' in data)
            location.href = `/?message=${JSON.stringify(data)}`
        else
            location.href = `/`
    })
}
else if (!token)
    initLoginPage()
else {
    fetch(`http://127.0.0.1:8000/api/user/getInfoPlayer/${token}`)
    .then(response => {
        if (!response.ok) {throw new Error('La requête a échoué');}return response.json(); })
    .then(data => {
        let p = document.createElement("p")
        let img = document.createElement("img")
        img.setAttribute("src", data.pic)
        img.style.height = "200px"
        p.innerText =`Bonjour ${data.username}`
        document.body.appendChild(img);
        document.body.appendChild(p);
})

    var h3 = document.createElement('h3')
    h3.innerHTML = "Login OK\n\n"
    document.body.appendChild(h3);
    document.body.appendChild(document.createElement('br'));
}