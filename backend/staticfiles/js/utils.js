/*function avec un tab, ou seul les user online peuvent acceder*/

const PATH_AVATAR_BACKEND = "static/avatars"

function	onlineDiv()
{return ['accountDiv', 'settingsDiv', 'friendsListDiv', "userProfileDiv", "searchDiv", "pongDiv", "tournamentDiv", "tournamentEditDiv"];}

/*function avec un tab, ou seul les user non online peuvent acceder*/
function	offlineDiv()
{return ["homeDiv", "signInDiv", "signUpDiv"];}

/*return div !none*/
function	findActiveDiv()
{
	const listDiv = onlineDiv().concat(offlineDiv());

	for (let i = 0; i < listDiv.length; i++)
	{
        const div = document.getElementById(listDiv[i]);
        if (div && div.style.display !== 'none')
            return listDiv[i];
	}
	return null;
}

/*Page for friends Profile*/
async function userDiv(divTo, userId)
{
    try {
        await friendProfile(userId);
        const div = document.getElementById(findActiveDiv());
        const divTarget = document.getElementById(divTo);

		div.style.display = 'none';
        divTarget.style.display = 'grid';
        changeNav(divTo);

        const addUrl = divTo.replace('Div', '');
        if (addUrl !== 'home')
            window.history.pushState(addUrl + 'Div', 'title', '/' + addUrl + '/' + userId);
    } catch (error) {
        console.error('Error in userDiv:', error);
    }
}

async function	changeDiv(divTo)
{
	clearInput();
	await statusOfPlayer(divTo)
	// statusFunction(divTo);

	const	currentDiv = findActiveDiv();
	var div = document.getElementById(currentDiv);
	var divTarget = document.getElementById(divTo);
	// if (!offlineDiv().includes(divTo))
	// 	await statusFunction(divTo);
	if (div)
		div.style.display = 'none';
	if (divTarget === settingsDiv)
		getPlayerInfo();
	else if (divTarget === accountDiv)
		await account();
	else if (divTo === 'pongDiv') {
		startPong(false);
		pongCanvasDiv.style.display = "none"
		pongChoise.style.display = "block"
	}
	else if (divTo === 'tournamentDiv')
		alreadyTournament();
	stopSocket()
	divTarget.style.display = 'block'
	changeNav(divTo);
	var addUrl = divTo.replace('Div', '');
	if (addUrl !== 'home')
		window.history.pushState(divTo, 'title', '/' + addUrl);
	else
		window.history.pushState(divTo, 'title', '/');
	return ;
}

function	clearInput()
{
	const arrayInput = ["username", "password",
						"username1", "email1", "password1",
						"confirm_password1", "avatar",
						"email2", "password2", "passwordNew2", "passwordNewConfirm", "codeMail2fa", "tournamentName", "alias", "numberOfPlayers"]

	arrayInput.forEach(function(element)
	{
		const inputElement = document.querySelector('input[name="'+ element+ '"]');
		if (inputElement)
			inputElement.value = '';
	})
	const errorMsg = document.querySelector('#errorMsg')
	if (errorMsg)
		errorMsg.remove();
}

function changeNav(activeDiv)
{
    const array = onlineDiv();
    const offlineNav = document.getElementById('noLogNav');
    const onlineNav = document.getElementById('LogNav');

    if (offlineNav && onlineNav)
	{
        if (array.indexOf(activeDiv) !== -1)
		{
            offlineNav.style.display = 'none';
            onlineNav.style.display = 'block';
        }
		else
		{
            offlineNav.style.display = 'block';
            onlineNav.style.display = 'none';
        }
    }
}

function	navEvent(toGo)
{
	const	div = onlineDiv().concat(offlineDiv());
	let findDisplayDiv = false;
	div.forEach(function(element)
	{
		var divCurrent = document.getElementById(element);
		if (divCurrent.style.display !== 'none' && !findDisplayDiv)
		{
			clearInput();
			changeDiv(toGo);
			findDisplayDiv = true;
		}
	})
}
function	changePageLoad(divName)
{
	const array = onlineDiv();
	const userId = sessionStorage.getItem('userID');
	if (array.includes(divName))
	{
		if (userId === null)
		{
			window.history.pushState('homeDiv', 'title', '/');
			divName = 'homeDiv';
		}
		else
		{
			var addUrl = divName.replace('Div', '');
			window.history.pushState(divName + 'Div', 'title', '/' + addUrl);
		}
	}
	else if (offlineDiv().includes(divName))
	{
		if (userId !== null)
		{
			window.history.pushState('accountDiv', 'title', '/account');
			divName = 'accountDiv';
		}

	}
	return divName;
}

function onPageLoad()
{
    let url = window.location.pathname;
	const words = url.split('/');
	let divName = words[1].replace('/', '') + 'Div';
    if (url !== "/")
	{
		divName = changePageLoad(divName);

        if (divName === 'friendsListDiv')
			friendsList();
		else if (words[1] === 'userProfile')
		{
			if (!sessionStorage.getItem('userID'))
				divName = 'homeDiv';
			else
			{
				userDiv('userProfileDiv', words[2]);
				divName = words[1] + 'Div';
				return ;
			}
		}
		else if (words[1] === 'account' && words[2])
		{
			if (!sessionStorage.getItem('userID'))
				divName = 'homeDiv';
			else
				divName = 'accountDiv';
		}
		else if (words[1] === 'tournament' && words[2])
		{
			if (!sessionStorage.getItem('userID'))
				divName = 'homeDiv';
			else
			{
				editTournamentFunction(words[2]);
				tournamentDiv('tournamentEditDiv', words[2]);
				return ;
			}
		}
		else if (divName === 'pongDiv' && words[2])
		{
			if (!sessionStorage.getItem('userID'))
				divName = 'homeDiv';
			else
			{
				pongDiv('pongDiv', words[2]);
				return ;
			}
		}

		if (divName)
		{
			changeDiv(divName);
		}
    }
	else
		changeDiv(changePageLoad('homeDiv'));
}

window.addEventListener("load", (event) => {
	clearInput();
	onPageLoad();
});

window.addEventListener("popstate", async function(event){
	clearInput();
	if (event.state === null) {
		return}
	if (offlineDiv().includes(event.state) && sessionStorage.getItem('userID'))
		await changeDiv2('accountDiv');
	else
		await changeDiv2(event.state);
	// window.history.back(event);
});


async function	changeDiv2(divTo)
{
	clearInput();
	await statusOfPlayer(divTo)
	// statusFunction(divTo);

	const	currentDiv = findActiveDiv();
	var div = document.getElementById(currentDiv);
	var divTarget = document.getElementById(divTo);
	// if (!offlineDiv().includes(divTo))
	// 	await statusFunction(divTo);
	if (div)
		div.style.display = 'none';
	if (divTarget === settingsDiv)
		getPlayerInfo();
	else if (divTarget === accountDiv)
		await account();
	else if (divTo === 'pongDiv')
		startSocket(false);
	else if (divTo === 'tournamentDiv')
		alreadyTournament();
	stopSocket()
	divTarget.style.display = 'block'
	changeNav(divTo);
	var addUrl = divTo.replace('Div', '');
	if (addUrl !== 'home')
		window.history.replaceState(divTo, 'title', '/' + addUrl);
	else
		window.history.replaceState(divTo, 'title', '/');
	return ;
}














