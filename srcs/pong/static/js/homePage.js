
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
	dayNight = localStorage.getItem("day-night");
	let r = document.querySelector(':root');
	if (dayNight == "night") {
		r.style.setProperty('--primary-color', '#dee2e6');
		r.style.setProperty('--seconde-color', '#adb5bd');
		r.style.setProperty('--text-color', '#232323');
		r.style.setProperty('--color-mode', 'day');
		console.log("-> day")
		localStorage.setItem("day-night", "day");

	}
	else {
		r.style.setProperty('--primary-color', '#0f0f0f');
		r.style.setProperty('--seconde-color', '#232323');
		r.style.setProperty('--text-color', '#dee2e6');
		r.style.setProperty('--color-mode', 'night');
		console.log("-> night")
		localStorage.setItem("day-night", "night");

	}
}

function logoutbtn(e){
	e.preventDefault()
	document.cookie = "PongToken=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;";
	location.href = "/"
}



function updateStat(){
	console.log("update")
	fetch(`http://127.0.0.1:8000/api/user/updateStatPlayer/${token}`)
	.then(response => {
		if (!response.ok) {throw new Error('La requête a échoué');} return response.json(); })
	.then(data => {
		console.log(data)
		document.getElementById('topBarNameBottom').innerText = `${data.elo} Elo (${data.win}/${data.loose})`;
	})
}

function listenIfupdateStat() {
    const targetElement = document.getElementById('topBarName');
    
    const observer = new MutationObserver((mutationsList, observer) => {
        for (let mutation of mutationsList) {
            if (mutation.type === 'attributes') {
                if (mutation.attributeName === 'needupdate') {
                    const needUpdateValue = mutation.target.getAttribute('needupdate');
                    if (needUpdateValue === "true") {
						console.log("update 3")
						targetElement.setAttribute("needupdate", "false")
						updateStat()
                    }
                }
            }
        }
    });
    
    const config = { attributes: true, attributeFilter: ['needupdate'] };
    observer.observe(targetElement, config);
}



function fillDataInPage(data) {
	
	document.getElementById('pongGame').style.display = 'block';
	document.getElementById('friends').style.display = 'block';
	document.getElementById('homePage').style.display = 'block';
	document.getElementById('topBarNameTop').innerText = data.username;
	document.getElementById('topBarNameBottom').innerText = `${data.elo} Elo (${data.victories}/${data.defeats})`;
	if (data.pic)
		document.getElementById('ppPlayer').setAttribute("src", data.pic)
	listenIfupdateStat()
	updateStat()
}


var token = getCookie('PongToken')

if (token) {
	fetch(`http://127.0.0.1:8000/api/user/getInfoPlayer`)
	.then(response => {
		if (!response.ok) {throw new Error('La requête a échoué');} return response.json(); })
	.then(data => {
		fillDataInPage(data)
		document.getElementById("btn-DN").addEventListener("click", e => 
			{ changeColorMode(e)})
		document.getElementById("btn-Logout").addEventListener("click", e => 
			{ logoutbtn(e)})
	})
}




// Establish a WebSocket connection
