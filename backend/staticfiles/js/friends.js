function	printErrorMsg2(formE2, data)
{
	let msgFromBack = '';
	if (data.error)
		msgFromBack = data.error;
	else if (data.message)
		msgFromBack = data.message;
	const errorMsg = document.querySelector('#errorMsg')
	if (errorMsg)
		errorMsg.remove();
	const newErrorMsg=document.createElement('p')
	if (data.message)
		newErrorMsg.style.color = 'green';
	else
		newErrorMsg.style.color = 'red';
	newErrorMsg.id = 'errorMsg';
	newErrorMsg.textContent = msgFromBack;
	formE2.insertAdjacentElement('beforeend', newErrorMsg);
}

function	sendFriendships(id)
{
	const csrftoken = getToken('csrftoken');
	fetch('/api/send/' + id,{
		method: 'POST',
		headers: {
			'X-CSRFToken': csrftoken,
			'Content-Type': 'application/json',
		},
	})
	.then(res => {
		return res.json();
	})
	.then(response => {
		updateToastMessage('Your friends Request sent successfully');
		onPageLoad();

	})
	.catch(error => {
		// console.log(error);
	})
}

//Page Friends
function userFriends(data)
{
    const friends = document.getElementById("friends");
    friends.innerHTML = '';
	var title = document.getElementById('titleFriends');
    title.innerHTML = `${data.friends.length} friend(s)`;

    const usernameList = document.createElement('div');
    usernameList.style.display = 'flex';
    usernameList.style.flexWrap = 'wrap';
	usernameList.style.justifyContent = 'center';

    for (let i = 0; i < data.friends.length; i++)
	{
        friendItem = document.createElement('div');
        friendItem.style.display = 'flex';
        friendItem.style.flexDirection = 'column';
        friendItem.style.alignItems = 'center';
        friendItem.style.padding = '10px 10px 38px 10px';
        friendItem.style.border = '1px solid #ccc';
        friendItem.style.borderRadius = '10px';
        friendItem.style.width = '50%';
		friendItem.style.maxWidth = '250px';

        const avatar = document.createElement('img');
		if (data.friends[i].avatar.includes(PATH_AVATAR_BACKEND))
			avatar.src = `${url}${data.friends[i].avatar}`;
		else
			avatar.src = data.friends[i].avatar;
        avatar.alt = `${data.friends[i].username}'s avatar`;
        avatar.style.width = '100%';
        avatar.style.height = '100%';
		avatar.style.borderRadius = '50%';
		avatar.style.cursor = 'pointer';
		if (data.friends[i].status_profile_str === "Offline")
			avatar.style.border = '4px solid grey';
		else if (data.friends[i].status_profile_str === "Online")
			avatar.style.border = '4px solid green';
		else
			avatar.style.border = '4px solid orange';
		avatar.onclick = function() {
			userProfile(data.friends[i].username);
		};


        const friendName = document.createElement('p');
        friendName.textContent = data.friends[i].username;
        friendName.style.color = 'black';
        friendName.style.textAlign = 'center';
		friendName.style.fontWeight = 'bold';
        friendName.style.fontSize = 'large';
        friendName.style.margin = '10px 0 5px 0';
        friendName.style.cursor = 'pointer';
		friendName.onclick = function() {
			userProfile(data.friends[i].username);
		};

        friendItem.appendChild(avatar);
        friendItem.appendChild(friendName);
        usernameList.appendChild(friendItem);
    }

    friends.appendChild(usernameList);
}

function	friendsList()
{
	if (!sessionStorage.getItem('userID'))
	{
		clearInput();
		changeDiv('signInDiv');
	}
	else
	{
		navEvent('friendsListDiv');
		const userID = sessionStorage.getItem('userID');

		fetch('/api/friends/' + userID, {
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
			userFriends(data);
		})
		.catch(error => {
			// console.error('There has been a problem with your fetch operation:', error);
		});
	}
}

//UserProfile
async function account1()
{
	if (!sessionStorage.getItem('userID'))
	{
		clearInput();
		changeDiv('signInDiv');
	}
	else
	{
		try {
			const response = await fetch('/api/players/me', {
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
			// console.error('There has been a problem with your fetch operation:', error);
		}
	}
}

async function unfriend(userId)
{
	// const csrftoken = getToken('csrftoken');
	try
	{
        const response = await fetch(`/api/unfriend/${userId}`,
		{
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getToken('csrftoken'),
            }
        });

        if (!response.ok) {
            throw new Error('Network response was not ok.');
        }
		else
		{
			const data = await response.json();
			updateToastMessage(data.message);
			onPageLoad();
		}
    }
	catch (error)
	{
        // console.error('There was a problem with the fetch operation:', error);
    }
}

async function cancelRequest(userId)
{
	// const csrftoken = getToken('csrftoken');
	try
	{
        const response = await fetch(`/api/cancel/${userId}`,
		{
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getToken('csrftoken'),
            }
        });

        if (!response.ok)
		{
			onPageLoad();
            throw new Error('Network response was not ok.');
        }
		else
		{
			const data = await response.json();
			// window.location.reload();
			updateToastMessage(data.message);
			onPageLoad();
			// sleep(3000);
		}

    }
	catch (error)
	{
        console.error('There was a problem with the fetch operation:', error);
    }
}
function updateToastMessage(message)
{
    const toastElement = document.getElementById('toast');
    if (!toastElement)
	{
        console.error('Toast element not found.');
        return;
    }

    const messageAlert = document.getElementById('messageAlert');
    if (!messageAlert)
	{
        console.error('Message alert element not found.');
        return;
    }

    messageAlert.textContent = message;

    const toast = new bootstrap.Toast(toastElement);
    toast.show();
}

/*profile du user rechercher ou friend profile*/
async function friendProfile(userId)
{
    try {
		let response = '';
		if (userId === sessionStorage.getItem('userID'))
			response = await fetch('/api/players/me');
		else
        	response = await fetch('/api/players/' + userId);
        if (!response.ok)
		{
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();

        const userMe = await account1();
		if (data.is_friend)
		{
			var friendsButton = document.createElement('button');
			friendsButton.innerHTML = '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-arrow-through-heart" viewBox="0 0 16 16"> <path fill-rule="evenodd" d="M2.854 15.854A.5.5 0 0 1 2 15.5V14H.5a.5.5 0 0 1-.354-.854l1.5-1.5A.5.5 0 0 1 2 11.5h1.793l.53-.53c-.771-.802-1.328-1.58-1.704-2.32-.798-1.575-.775-2.996-.213-4.092C3.426 2.565 6.18 1.809 8 3.233c1.25-.98 2.944-.928 4.212-.152L13.292 2 12.147.854A.5.5 0 0 1 12.5 0h3a.5.5 0 0 1 .5.5v3a.5.5 0 0 1-.854.354L14 2.707l-1.006 1.006c.236.248.44.531.6.845.562 1.096.585 2.517-.213 4.092-.793 1.563-2.395 3.288-5.105 5.08L8 13.912l-.276-.182a22 22 0 0 1-2.685-2.062l-.539.54V14a.5.5 0 0 1-.146.354zm2.893-4.894A20.4 20.4 0 0 0 8 12.71c2.456-1.666 3.827-3.207 4.489-4.512.679-1.34.607-2.42.215-3.185-.817-1.595-3.087-2.054-4.346-.761L8 4.62l-.358-.368c-1.259-1.293-3.53-.834-4.346.761-.392.766-.464 1.845.215 3.185.323.636.815 1.33 1.519 2.065l1.866-1.867a.5.5 0 1 1 .708.708z"/> </svg>Friends';
			document.getElementById('frRelation').innerHTML = '';
			friendsButton.style.backgroundColor = 'cornflowerblue';
			friendsButton.style.color = 'white';
			var	unfriendButton = document.createElement('button');
			unfriendButton.innerHTML = 'unfriend';
			unfriendButton.style.backgroundColor = 'transparent';
			unfriendButton.style.borderColor = 'transparent';
			unfriendButton.style.textDecoration = 'underline black';
			unfriendButton.onclick = async function()
			{
				await unfriend(userId);
			};

			document.getElementById('frRelation').appendChild(friendsButton);
			document.getElementById('frRelation').appendChild(unfriendButton);
		}
		else if (data.is_self)
		{
			var youButton = document.createElement('button');
			youButton.innerHTML = 'You';
			// document.getElementById('relationStatus').innerHTML = 'Myself';
			document.getElementById('frRelation').innerHTML = '';
			document.getElementById('frRelation').appendChild(youButton);
		}
		else if (data.request_sent_status === 1 && !data.is_friend)
		{
			var requestSentButton = document.createElement('button');
			requestSentButton.innerHTML = '';
            requestSentButton.innerHTML = '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-send" viewBox="0 0 16 16"> <path d="M15.854.146a.5.5 0 0 1 .11.54l-5.819 14.547a.75.75 0 0 1-1.329.124l-3.178-4.995L.643 7.184a.75.75 0 0 1 .124-1.33L15.314.037a.5.5 0 0 1 .54.11ZM6.636 10.07l2.761 4.338L14.13 2.576zm6.787-8.201L1.591 6.602l4.339 2.76z"/> </svg> Request Sent';
            requestSentButton.disabled = true;
            document.getElementById('frRelation').innerHTML = '';
			var	cancel = document.createElement('button');
			cancel.innerHTML = 'cancel request';
			cancel.style.backgroundColor = 'transparent';
			cancel.style.borderColor = 'transparent';
			cancel.style.textDecoration = 'underline black';
			cancel.onclick = async function()
			{
				await cancelRequest(userId);
			};
            document.getElementById('frRelation').appendChild(requestSentButton);
			document.getElementById('frRelation').appendChild(cancel);
		}
		else if (data.request_sent_status === 0 && !data.is_friend)
		{
			var requestSentButton = document.createElement('button');
			requestSentButton.innerHTML = '';
            requestSentButton.innerHTML = '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-send" viewBox="0 0 16 16"> <path d="M15.854.146a.5.5 0 0 1 .11.54l-5.819 14.547a.75.75 0 0 1-1.329.124l-3.178-4.995L.643 7.184a.75.75 0 0 1 .124-1.33L15.314.037a.5.5 0 0 1 .54.11ZM6.636 10.07l2.761 4.338L14.13 2.576zm6.787-8.201L1.591 6.602l4.339 2.76z"/> </svg> Request Sent';
            requestSentButton.disabled = true;
            document.getElementById('frRelation').innerHTML = '';
            document.getElementById('frRelation').appendChild(requestSentButton);
		}
		else if (data.request_sent_status === -1 && !data.is_friend)
		{
			var notFriendsButton = document.createElement('button');
			notFriendsButton.onclick = function() {
				sendFriendships(userId);
			};
			notFriendsButton.innerHTML = '';
			notFriendsButton.innerHTML = '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-person-add" viewBox="0 0 16 16"> <path d="M12.5 16a3.5 3.5 0 1 0 0-7 3.5 3.5 0 0 0 0 7m.5-5v1h1a.5.5 0 0 1 0 1h-1v1a.5.5 0 0 1-1 0v-1h-1a.5.5 0 0 1 0-1h1v-1a.5.5 0 0 1 1 0m-2-6a3 3 0 1 1-6 0 3 3 0 0 1 6 0M8 7a2 2 0 1 0 0-4 2 2 0 0 0 0 4"/> <path d="M8.256 14a4.5 4.5 0 0 1-.229-1.004H3c.001-.246.154-.986.832-1.664C4.484 10.68 5.711 10 8 10q.39 0 .74.025c.226-.341.496-.65.804-.918Q8.844 9.002 8 9c-5 0-6 3-6 4s1 1 1 1z"/> </svg> Friend Request';
			notFriendsButton.style.backgroundColor = 'green';
			notFriendsButton.style.color = 'white';
			notFriendsButton.style.borderColor = 'black';
			document.getElementById('frRelation').innerHTML = '';
			document.getElementById('frRelation').appendChild(notFriendsButton);
		}
        document.getElementById('frName').innerHTML = data.data.username;
		document.getElementById('frEmail').innerHTML = data.data.email;
        document.getElementById('frDate').innerHTML = data.data.date_joined;
        document.getElementById('frFriend').innerHTML = data.data.friend_count;
        document.getElementById('frPlayed').innerHTML = data.data.games_played;
        document.getElementById('frVictories').innerHTML = data.data.victories;
        document.getElementById('frDefeats').innerHTML = data.data.defeats;
		document.getElementById('frElo').innerHTML = data.data.elo;
		document.getElementById('frScore').innerHTML = data.data.score;
        if (data.data.status_profile_str === 'Online') {
            document.getElementById('frStatus').style.backgroundColor = 'green';
        }
		else if (data.data.status_profile_str === 'Offline') {
            document.getElementById('frStatus').style.backgroundColor = 'grey';
        }
		else
			document.getElementById('frStatus').style.backgroundColor = 'orange';

        var avatarImg = document.querySelector('#frAvatar img');

		historyTournament('tournamentHistoryFriend');
		historyMatch('matchHistoryFriend');

		if (data.data.avatar.includes(PATH_AVATAR_BACKEND))
			avatarImg.src = `${url}${data.data.avatar}`;
		else
			avatarImg.src = data.data.avatar;
        createChart1(data.data.victories, data.data.defeats);
		let tmp = await dashboard(data.data.id);
		createChart4(tmp);
		createChart5(await dashboard(sessionStorage.getItem('userID')), await dashboard(data.data.id));
		// createChart4(data);

    } catch (error) {
        console.error('Error fetching user ID:', error);
    }
}

async function userProfile(username)
{
    try
	{
        const response = await fetch('/api/getuserid/' + username);
        const data = await response.json();
        await friendProfile(data.id);
        userDiv("userProfileDiv", data.id);
    } catch (error) {
        console.error('Error fetching user ID:', error);
    }
}


	function acceptFriendships(senderId)
	{
		const csrftoken = getToken('csrftoken');
		fetch(`/api/accept/${senderId}`, {
			method: 'POST',
			headers: {
				'X-CSRFToken': csrftoken,
				'Content-Type': 'application/json'
			}
		})
		.then(response => {
			return response.json();
		})
		.then(data => {
			removeNotif(data.id)

			const dropdownMenu = document.getElementById('notify');
			const notificationItems = dropdownMenu.getElementsByTagName('li');

			if (notificationItems.length === 0) {
				var badgeElement = document.getElementById('notificationBadge');
				badgeElement.className = '';

				var badgeElement2 = document.getElementById('notificationBadge2');
				badgeElement2.className = '';
			}

		})
		.catch(error => {
			console.error('Error accepting friendship:', error);
		});

	}

	function rejectFriendships(senderId)
	{
		const csrftoken = getToken('csrftoken');
		fetch(`api/reject/${senderId}`, {
			method: 'POST',
			headers: {
				'X-CSRFToken': csrftoken,
				'Content-Type': 'application/json'
			}
		})
		.then(response => response.json())
		.then(data => {
			removeNotif(data.id);
			// onPageLoad();
		})
		.catch(error => {
			console.error('Error accepting friendship:', error);
		});

	}


	function handleAcceptButtonClick(message)
	{
		// return function() {
		let senderId;
		try
		{
			if (message.sender && message.sender.id)
			{
				senderId = message.sender.id;
			}
		} catch (error) {
			console.error('Error parsing message data:', error);
		}
		if (senderId) {
			acceptFriendships(senderId);
		} else {
			console.error('Sender ID not found in message:', message);
		}
		// };
	}

	function handleRejectButtonClick(message)
	{
		let senderId;
		try {
			if (message.sender && message.sender.id) {
				senderId = message.sender.id;
			}
		} catch (error) {
			console.error('Error parsing message data:', error);
		}
		if (senderId) {
			rejectFriendships(senderId);
		} else {
			console.error('Sender ID not found in message:', message);
		}
	}

	function updateInitialMessage(newMessage)
	{
        var messageElement = document.getElementById('initialMessage');
        messageElement.textContent = JSON.stringify(newMessage, null, 4);
    }

	function createNotificationListItem(message)
	{
		var newLi = document.createElement('div');
		newLi.style.display = 'flex';
		newLi.style.alignItems = 'center';
		// newLi.style.marginLeft = '20px';
		newLi.style.position = 'relative';
		newLi.style.margin = '15px';
		// newLi.style.left = '150px';
		// newLi.style.margin = '15px';

		// Avatar
		var avatarContainer = document.createElement('div');
		// avatarContainer.style.marginRight = '10px'; // Marge entre l'avatar et le texte
		var avatarNotif = document.createElement('img');
		avatarNotif.className = 'imgNotif';
		avatarNotif.width = '65%';
		if (message.sender.avatar.includes(PATH_AVATAR_BACKEND))
			avatarNotif.src = `${url}${message.sender.avatar}`;
		else
			avatarNotif.src = message.sender.avatar;

		avatarNotif.alt = message.sender.username + "'s avatar";
		avatarNotif.onclick = function() {
			userProfile(message.sender.username);
		};
		avatarNotif.style.borderRadius = '10px';
		avatarContainer.appendChild(avatarNotif);
		newLi.appendChild(avatarContainer);

		var messageContainer = document.createElement('div');
		var p = document.createElement('p');
		p.innerHTML = message.message;
		p.className = "message";
		messageContainer.appendChild(p);
		// newLi.appendChild(messageContainer);

		// Actions (Accepter / Rejeter)
		if (message.message !== 'Your friend request has been accepted')
		{
			// var actionsContainer = document.createElement('div');
			var acceptButton = document.createElement('button');
			acceptButton.className = 'btn btn-success btn-sm accept-button';
			acceptButton.textContent = 'Accept';
			acceptButton.style.marginLeft = '10px';

			acceptButton.onclick = function() {
				handleAcceptButtonClick(message);
			};

			var rejectButton = document.createElement('button');
			rejectButton.className = 'btn btn-danger btn-sm reject-button';
			rejectButton.textContent = 'Reject';
			rejectButton.onclick = function() {
				handleRejectButtonClick(message);
			};

			messageContainer.appendChild(acceptButton);
			messageContainer.appendChild(rejectButton);
		}

		newLi.appendChild(messageContainer);
		var separator = document.createElement('hr');
		separator.className = 'dropdown-divider';
		newLi.appendChild(separator);

		if (message.message === 'Your friend request has been accepted')
		{
			onPageLoad();
		}
		return newLi;
	}

	function removeNotif(id)
	{
		const divId = document.getElementById(id);
		const ulId = document.getElementById('notify');

		// divId.innerHTML = '';
		ulId.removeChild(divId);

		const dropdownMenu = document.getElementById('notify');
		const notificationItems = dropdownMenu.getElementsByTagName('li');

		if (notificationItems.length === 0) {
			var badgeElement = document.getElementById('notificationBadge');
			badgeElement.className = 'visually-hidden';

			var badgeElement2 = document.getElementById('notificationBadge2');
			badgeElement2.className = 'visually-hidden';
		}
	}

	async function setMessage(message, id) {

		var notificationListItem = createNotificationListItem(message);
		notificationListItem.id = id;
		var ulElement = document.getElementById('notify');
		if (ulElement) {
			ulElement.appendChild(notificationListItem);
			var badgeElement = document.getElementById('notificationBadge');
			var badgeElement2 = document.getElementById('notificationBadge2');
			if (badgeElement.classList.contains('visually-hidden')) {
				badgeElement.className = 'position-absolute top-0 start-100 translate-middle p-2 bg-danger border-light rounded-circle';
			}
			if (badgeElement2.classList.contains('visually-hidden')) {
				badgeElement2.className = 'position-absolute top-0 start-100 translate-middle p-2 bg-danger border-light rounded-circle';
			}
		} else {
			console.error("Notification list element 'notify' not found.");
		}
		return ;
	}
