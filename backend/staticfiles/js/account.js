function getCSRFToken() {
	const cookieValue = document.cookie.match('(^|;)\\s*' + 'csrftoken' + '\\s*=\\s*([^;]+)');
	return cookieValue ? cookieValue.pop() : '';
}

const url = window.location.protocol + "//" + window.location.hostname + ":" + window.location.port + "/";


function backSetting()
{
	navEvent('settingsDiv');
    fetch('/api/players/me', {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
		if (data.data.is_42_user === false)
		{
			let input = document.getElementById('playerName');
			input.disabled = false;
        	input.value = data.data.username;
		}
		else
		{
			document.getElementById('playerName').placeholder = data.data.username;
		if (data.data.tfaActive)
			btnSendMail2fa.setAttribute("disabled", "")
			document.getElementById('playerName').value = data.data.username;
			let input = document.getElementById('playerName');
			input.disabled = true;
			let cpPassword = document.getElementById('cpPassword');
			cpPassword.disabled = true;
			let cpPasswordNew = document.getElementById('cpPasswordNew');
			cpPasswordNew.disabled = true;
			let cpPasswordNewConfirm = document.getElementById('cpPasswordNewConfirm');
			cpPasswordNewConfirm.disabled = true;
			let changePassword = document.getElementById('changePassword')
			changePassword.style.display = 'none';
		}
        document.getElementById('playerEmail').placeholder = data.data.email;
		const avatarElement = document.getElementById('currentAvatar');
        if (avatarElement) {
			if (data.data.avatar.includes(PATH_AVATAR_BACKEND))
				{
					console.log(data.data.avatar);
					console.log(url);
					console.log(`${url}${data.data.avatar}`);
					avatarElement.src = `${url}${data.data.avatar}`;
				}
		
			else
				avatarElement.src = data.data.avatar;

		}
		document.getElementById('playerAvatar').placeholder = data.data.avatar;
		// sessionStorage.setItem('userID', data.data.id);
		// document.cookie = `userID=${data.data.id}`;
    })
    .catch(error => {
		console.error('There has been a problem with your fetch operation:', error);
    });
}
function getPlayerInfo()
{
	if (!sessionStorage.getItem('userID'))
	{
		clearInput();
		changeDiv('signInDiv');
	}
	else
	{
		backSetting();
	}

}

async function account()
{
	if (sessionStorage.getItem('userID') === 'empty')
	{
		sessionStorage.setItem('userID', 'connect');
		return;
	}
	else if (!sessionStorage.getItem('userID'))
	{
		clearInput();
		changeDiv('signInDiv');
	}
	else
	{
		navEvent('accountDiv');
		await fetch('/api/players/me', {
			method: 'GET',
			headers: {
				'Content-Type': 'application/json'
			}
		})
		.then(async response => {
			if (!response.ok) {
				throw new Error('Network response was not ok');
			}
			return response.json();
		})
		.then(async data => {
			document.getElementById('accountName').innerHTML = data.data.username;
			document.getElementById('accountEmail').innerHTML = data.data.email;
			document.getElementById('accountDate').innerHTML = data.data.date_joined;
			document.getElementById('accountFriend').innerHTML = data.data.friend_count;
			document.getElementById('accountPlayed').innerHTML = data.data.games_played;
			document.getElementById('accountVictories').innerHTML = data.data.victories;
			document.getElementById('accountDefeats').innerHTML = data.data.defeats;
			document.getElementById('accountElo').innerHTML = data.data.elo;
			document.getElementById('accountScore').innerHTML = data.data.score;
			document.getElementById('accountTournament').innerHTML = data.data.tournaments_won;
			if (data.data.status_profile_str === 'Offline')
			{
				document.getElementById('accountStatus').style.backgroundColor = 'grey';
			}
			else if (data.data.status_profile_str === 'Online')
				document.getElementById('accountStatus').style.backgroundColor = 'green';
			else
				document.getElementById('accountStatus').style.backgroundColor = 'orange';

			var avatarImg = document.querySelector('#accountAvatar img');
			if (data.data.avatar.includes(PATH_AVATAR_BACKEND))
			{
				avatarImg.src = `${url}${data.data.avatar}`;
			}
			else
			{
				avatarImg.src = data.data.avatar;
			}
			sessionStorage.setItem('userID', data.data.id);
			document.cookie = `userID=${data.data.id}`;
			historyTournament('tournamentHistory');
			historyMatch('matchHistory');
			createChart(data.data.victories, data.data.defeats);
			let tmp = await dashboard(sessionStorage.getItem('userID'));
			createChart3(tmp);
		})
		.catch(error => {
			console.error('There has been a problem with your fetch operation:', error);
		});
	}
}

async function dashboard(userID) {
    try {
        const response = await fetch('/api/dashboard/' + userID, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
        });

        if (!response.ok) {
            throw new Error('Network response was not ok');
        }

        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Error fetching dashboard data:', error);
        throw error;
    }
}


function confirmEdit()
{
	const updatedName = document.getElementById('playerName').value;
	if (!updatedName)
	{
		const formE2 = document.querySelector("form.editProfile");
        const errorData = { error: 'Le champ du nom est vide.' };

        printErrorMsg(formE2, errorData);
        return;
	}
	const updatedEmail = document.getElementById('playerEmail').placeholder;
	const userId = sessionStorage.getItem('userID');
	let userAvatar = document.getElementById('playerAvatar').files[0];

	const allowedTypes = ['image/jpeg', 'image/jpg', 'image/png'];
	const maxFileSize = 10 * 1024 * 1024; // 10MB
	if (userAvatar)
	{
		if (!allowedTypes.includes(userAvatar.type)) {
			const formE2 = document.querySelector("form.editProfile");
			const errorData = {error: 'Invalid file type. Only JPEG and PNG are allowed'};
			printErrorMsg(formE2, errorData);
			userAvatar = null;
			return ;
		}
		else if (userAvatar.size > maxFileSize) {
			const formE2 = document.querySelector("form.editProfile");
			const errorData = {error:'File size exceeds 10 MB'};
			printErrorMsg(formE2, errorData);
			userAvatar = null;
			return ;
		}
		else {
			const imageURL = URL.createObjectURL(userAvatar);
			userAvatar = imageURL;
		}
	}
	else
	{
		const imgSrc = document.getElementById('currentAvatar');
		userAvatar = imgSrc.src;
	}

	const csrftoken = getToken('csrftoken');
	const formData = new FormData();
	formData.append('username', updatedName);
	formData.append('email', updatedEmail);
	formData.append('avatar', document.getElementById('playerAvatar').files[0]);
	fetch('/api/edit/' + userId, {
		method: 'POST',
		headers: {
			'X-CSRFToken': csrftoken,
				},
		body: formData
	})
	.then(response => {
		return response.json();
	})
	.then(data => {
		document.getElementById('playerEmail').disabled = true;
		const avatarElement = document.getElementById('currentAvatar');
        if (avatarElement)
		{
            avatarElement.src = userAvatar;
		}
		const formEl = document.querySelector("form.editProfile");
		printErrorMsg(formEl, data);
	})
	.catch(error => {
		console.error('There has been a problem with your fetch operation:', error);
	});
}

function changePassword()
{
	const password = document.getElementById('cpPassword').value;
	const newPassword = document.getElementById('cpPasswordNew').value;
	const confirmNewPassword = document.getElementById('cpPasswordNewConfirm').value;
	const userId = sessionStorage.getItem('userID');
	const csrftoken = getToken('csrftoken');


	fetch('/api/change-password/' + userId, {
		method: 'POST',
		headers: {
			'X-CSRFToken': csrftoken,
			'Content-Type': 'application/json',
		},
		body: JSON.stringify({
			old_password: password,
			new_password: newPassword,
			confirm_password: confirmNewPassword
		})
	})
	.then(response => {
		if (!response.ok) {
			const formE1 = document.querySelector("form.changePassword");
			printErrorMsg(formE1, response);
		}
		return response.json();
	})
	.then(data => {
		const formE1 = document.querySelector("form.changePassword");
		printErrorMsg(formE1, data);
	})
	.catch(error => {
		// console.log(error);
	});
}



document.addEventListener('DOMContentLoaded', function()
{
	if (window.location.pathname === '/settings')
	{
		const changePasswordBtn = document.getElementById('changePassword');

		if (changePasswordBtn) {
			changePasswordBtn.addEventListener('click', event => {
				event.preventDefault();
				changePassword();
			});
		}
	}
});

async function changeStatus() {
    try {
        const userId = sessionStorage.getItem('userID');

		if (!userId || userId === 'connect')
		{
			return ;
		}
        const response = await fetch(`/api/change-status/${userId}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getToken('csrftoken')
            }
        });

        if (!response.ok) {
            throw new Error('Network response was not ok');
        }

        const data = await response.json();
    } catch (error) {
        console.error('There was a problem with the fetch operation:', error);
    }
}

async function statusUser() {
	try {
		const userId = sessionStorage.getItem('userID');
		if (!userId || userId === 'connect')
		{
			return ;
		}
		const response = await fetch('/api/get-status', {
			method: 'GET',
			headers: {
				'Content-Type': 'application/json',
				'X-CSRFToken': getToken('csrftoken')
			}
		});

		if (!response.ok) {
			throw new Error('Network response was not ok');
		}

		const data = await response.json();
		return (data.status);

	} catch (error) {
		// console.error('There was a problem with the fetch operation:', error);
	}
}

async function	statusFunction(divTo)
{
	const userId = sessionStorage.getItem('userID');
	if (!userId || userId === 'connect')
	{
		return ;
	}
	const status = await statusUser();

    const userStatus = status.status;

    // const currentDiv = findActiveDiv();

    if (divTo === 'pongDiv' && userStatus === 1)
	{
        await changeStatus();
    }
	else if (divTo !== 'pongDiv' && userStatus === 2)
	{
		await changeStatus();
	}
	return ;
}

async function statusOfPlayer(divTo)
{
	const offline = offlineDiv();
	const online = onlineDiv();

	const status = await statusUser();
	if (status === 0 && online.includes(divTo))//OFFLINE
	{
		await changeStatusRefresh();
	}
	else if (status === 1 && offline.includes(divTo))//ONLINE
	{
		await changeStatusRefresh();
	}
	else if (divTo === 'pongDiv' && status !==2)
	{
		await changeStatus();
	}
	else if (status === 2 && divTo !== 'pongDiv' && !offline.includes(divTo))
	{
		await changeStatus();
	}
	const tmp = await statusUser();
	return ;
}


async function changeStatusRefresh() {
    try {
        const userId = sessionStorage.getItem('userID');

		if (!userId || userId === 'connect')
			return ;

			const response = await fetch(`/api/changeStatusRefresh/${userId}`, {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json',
					'X-CSRFToken': getToken('csrftoken')
				}
			});

			if (!response.ok) {
				throw new Error('Network response was not ok');
			}

			const data = await response.json();
    } catch (error) {
        // console.error('There was a problem with the fetch operation:', error);
    }
}


	window.addEventListener('beforeunload', () => {
		if (sessionStorage.getItem('userID'))
			changeStatusRefresh();
	});



const btnSendMail2fa = document.getElementById("btnSendMail2fa")
const modal2faactive = document.getElementById("modal2faactive")
var modalElement = new bootstrap.Modal(modal2faactive);
const activeModalBtn2fa = document.getElementById("activeModalBtn2fa")
const codeMail2fa = document.getElementById("codeMail2fa")


btnSendMail2fa.addEventListener("click", e => {
	fetch('/api/tfaSendMail/',{
		method: 'POST',
		headers: {
			'Content-Type': 'application/json',
			'X-CSRFToken': getCSRFToken(),
		}})
	.then(res => res.json())
	.then(data => {
		if ("ok" in data)
		{
			clearInput();
			modalElement.show();
			modal2faactive.setAttribute("data-id", data.ok)
		}
		else
		{
			const formE2 = document.querySelector("form.editProfile");
			printErrorMsg(formE2, data);
		}
	})
} )

activeModalBtn2fa.addEventListener("click", e => {
	fetch('/api/tfaSetActive/',{
		method: 'POST',
		headers: {
			'Content-Type': 'application/json',
			'X-CSRFToken': getCSRFToken(),
		},
		body:JSON.stringify({"id":modal2faactive.getAttribute("data-id"), "code": codeMail2fa.value})})
	.then(res => res.json())
	.then(data => {
		if ("message" in data)
		{
			modal2faactive.setAttribute("data-id", data.ok)
			const formE2 = document.querySelector("form.editProfile");
			printErrorMsg(formE2, data);
			modalElement.hide();
		}
		else
		{
			const form = document.getElementById('form2fa');
			printErrorMsg(form, data);
		}
	})
} )

function	boucle(data)
{
	let playerList = '';

	if (Array.isArray(data.tournament_players)) {
        data.tournament_players.forEach(player => {
			if (playerList !== '')
            	playerList += ', ' + player.username;
			else
				playerList += player.username;
        });
    }
	return (playerList);
}

function	historyTournament(id)
{
	const userID = sessionStorage.getItem('userID');
	fetch('/api/tournamentsList/' + userID, {
		method: 'GET',
		headers: {
			'X-CSRFToken': getToken('csrftoken'),
			'Content-Type': 'application/json'
		}
	})
	.then(response => {
		return response.json();
	})
	.then(data =>
	{
		const tournamentHistory = document.getElementById(id);
        tournamentHistory.innerHTML = '';

        data.forEach(tournament => {
            const listItem = document.createElement('li');
			const playerList = boucle(tournament);
            listItem.innerHTML = `
                <strong>Name of tournament:</strong> ${tournament.name}<br>
                <strong>Date creation:</strong> ${new Date(tournament.date_joined).toLocaleDateString()}<br>
                <strong>Players:</strong> ${playerList}<br>
				<strong>Numbers of players:</strong> ${tournament.numberOfPlayer}<br>
				<strong>Winner:</strong> ${tournament.winner}<br><br>
            `;
			// avatar.onclick = function() {
            //     userProfile(i.username);
            // };
			listItem.onclick = function() {
				tournamentDiv('tournamentEditDiv', tournament.id);
			};
			listItem.id = 'coucou';
            tournamentHistory.appendChild(listItem);
        });
	})
}
function	historyMatch(id)
{
	const userID = sessionStorage.getItem('userID');
	fetch('/api/matchList/' + userID, {
		method: 'GET',
		headers: {
			'X-CSRFToken': getToken('csrftoken'),
			'Content-Type': 'application/json'
		}
	})
	.then(response => {
		return response.json();
	})
	.then(data =>
	{
		const matchHistory = document.getElementById(id);
        matchHistory.innerHTML = '';
        data.matches.forEach(match => {
            const listItem = document.createElement('li');
            listItem.innerHTML = `
				<strong>Date:</strong> ${new Date(match.end_time).toLocaleDateString()}<br>
                ${match.player1} <strong> VS </strong> ${match.player2}<br>
				<strong> ${match.player1} Score:</strong> ${match.score_player1}<br>
				<strong> ${match.player2} Score:</strong> ${match.score_player2}<br>
                <strong>Winner:</strong> ${match.winner}<br><br>
            `;
            matchHistory.appendChild(listItem);
        });
	})
}
