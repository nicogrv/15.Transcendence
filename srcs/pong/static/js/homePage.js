console.log("test")

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


function changeColorMode(e){
	e.preventDefault()
	let r = document.querySelector(':root');
	let mode = getComputedStyle(r).getPropertyValue('--color-mode')
	if (mode == "night") {
		r.style.setProperty('--primary-color', '#dee2e6');
		r.style.setProperty('--seconde-color', '#adb5bd');
		r.style.setProperty('--text-color', '#232323');
		r.style.setProperty('--color-mode', 'day');
	}
	else {
		r.style.setProperty('--primary-color', '#0f0f0f');
		r.style.setProperty('--seconde-color', '#232323');
		r.style.setProperty('--text-color', '#dee2e6');
		r.style.setProperty('--color-mode', 'night');
	}
}

function logoutbtn(e){
	e.preventDefault()
	document.cookie = "PongToken=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;";
	location.href = "/"
}

function fillDataInPage(data) {
	document.getElementById('homePage').style.display = 'block';
	document.getElementById('topBarNameTop').innerText = data.username;
	document.getElementById('topBarNameBottom').innerText = `${data.elo} Elo (${data.victories}/${data.defeats})`;
	if (data.pic)
		document.getElementById('ppPlayer').setAttribute("src", data.pic)
}


var token = getCookie('PongToken')

if (token) {
	console.log("1")
	fetch(`http://127.0.0.1:8000/api/user/getInfoPlayer`)
	.then(response => {
		if (!response.ok) {throw new Error('La requête a échoué');}return response.json(); })
	.then(data => {
		console.log("2")
		fillDataInPage(data)
		document.getElementById("btn-DN").addEventListener("click", e => 
			{ changeColorMode(e)}) // btn change color page
		document.getElementById("btn-Logout").addEventListener("click", e => 
			{ logoutbtn(e)})
		console.log("3")
	})
		console.log("4")
	
}


// Establish a WebSocket connection
