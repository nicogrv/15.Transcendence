
const loginPage = document.getElementById('loginPage');
const btnLog42 = document.getElementById('btnLog42');
btnLog42.addEventListener("click", (e) => {
    location.href = ("https://api.intra.42.fr/oauth/authorize?client_id=u-s4t2ud-9198daa6a4877961ff5b7a3ca58e5990fd4f618ddc61420e8aa18e18ed316472&redirect_uri=http%3A%2F%2F127.0.0.1%3A8000%2F&response_type=code")
})

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
    }, timeDeleteAlerte);
}

var token = getCookie('PongToken')
var messageQuery = getParameterValue('message')
queryValueCode = getParameterValue("code")


console.log("Token récupéré : ", token);
console.log("queryValueCode: ", queryValueCode)
if (messageQuery)
{
    loginPage.style.display = 'block'
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
    loginPage.style.display = 'block'
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