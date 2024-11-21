
const urlParams = new URLSearchParams(window.location.search);
const code = urlParams.get('code');
var uid = undefined


document.addEventListener('DOMContentLoaded', async function()
{
	if (window.location.pathname === '/account' && !sessionStorage.getItem('userID'))
		{
		let homeDiv = document.getElementById('homeDiv');
		homeDiv.className = "container content";
		let noLogHome = document.getElementById('noLogHome');
		noLogHome.style.display = 'none';
		let spinners = document.getElementById('spinners');
		spinners.style.display = 'block';
		if (code) {
			sendToFtAuth()
		}
	}
});



document.getElementById("activeModalBtn2fa42").addEventListener("click", e => {
	sendToFtAuth()
})

function sendToFtAuth() {
	fetch(`/api/authWithFortyTwo?code=${code}`, {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json',
			'X-CSRFToken': getToken('csrftoken'),
		},
		body:JSON.stringify({"uid":uid, "tfaCode": document.getElementById("codeMail2fa42").value})

	})
	.then(response => {
		return response.json();
	})
	.then(async data => {
		if ("error" in data)
		{
			const form = document.getElementById('formHome');
			printErrorMsg(form, data);
			return ;
			// $('#modal2fa42').modal('hide')
		}
		$('#modal2fa42').modal('hide')
		if (data.tfa) {
			uid = data.tfa
			$('#modal2fa42').modal('show')
		}
		if (data.access) {
			document.cookie = `access=${data.access}; Secure; SameSite=Strict;`;
			document.cookie = `refresh=${data.refresh}; Secure; SameSite=Strict;`;
			spinners.style.display = 'none';
			homeDiv.className = "";
			sessionStorage.setItem('userID', 'empty');
			await account();
			changeDiv('accountDiv')

		}
	})
	.catch(error => {
	});
}
