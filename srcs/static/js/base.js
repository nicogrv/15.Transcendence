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
    
    const divUsername = document.createElement('div');
    divUsername.classList.add('mb-3');
    
    const labelUsername = document.createElement('label');
    labelUsername.setAttribute('for', 'exampleInputEmail1');
    labelUsername.classList.add('form-label');
    labelUsername.textContent = 'Username';
    
    const inputUsername = document.createElement('input');
    inputUsername.setAttribute('type', 'email');
    inputUsername.classList.add('form-control');
    inputUsername.setAttribute('id', 'exampleInputEmail1');
    inputUsername.setAttribute('aria-describedby', 'emailHelp');
    
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
        location.href = ("https://api.intra.42.fr/oauth/authorize?client_id=u-s4t2ud-9198daa6a4877961ff5b7a3ca58e5990fd4f618ddc61420e8aa18e18ed316472&redirect_uri=http%3A%2F%2F127.0.0.1%3A8000%2Fapi%2Fauth%2FauthWithFortyTwo&response_type=code")
    })
    
    
    const btnSign42 = document.createElement('button');
    btnSign42.setAttribute('type', 'submit');
    btnSign42.classList.add('btn-css', 'btn-Log42');
    btnSign42.textContent = 'Sign with 42';
    
    // Ajout des éléments au DOM
    divSignInUp42Flex.appendChild(divSignInUp42);
    divSignInUp42.appendChild(formContainerGreen);
    formContainerGreen.appendChild(formLogin);
    formLogin.appendChild(h3Login);
    formLogin.appendChild(divUsername);
    divUsername.appendChild(labelUsername);
    divUsername.appendChild(inputUsername);
    formLogin.appendChild(divPassword);
    divPassword.appendChild(labelPassword);
    divPassword.appendChild(inputPassword);
    formLogin.appendChild(submitButton);
    divSignInUp42.appendChild(btnLog42);
    btnLog42.appendChild(btnSign42);
    
    // Ajout du formulaire "Sign in" à côté du formulaire "Login"
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
    formSignIn.appendChild(divUsername.cloneNode(true)); // Reuse the username input
    formSignIn.appendChild(divPassword.cloneNode(true)); // Reuse the password input
    formSignIn.appendChild(divConfirmPassword);
    divConfirmPassword.appendChild(labelConfirmPassword);
    divConfirmPassword.appendChild(inputConfirmPassword);
    formSignIn.appendChild(submitButtonPink);
    
    // Ajout de la structure créée au document

    document.body.appendChild(divSignInUp42Flex);
    
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
var token = getCookie('PongToken')
console.log("Token récupéré : ", token);

if (!token)
    initLoginPage()
else {
    var h3 = document.createElement('h3')
    h3.innerHTML = "Login OK"
    document.body.appendChild(h3);
}