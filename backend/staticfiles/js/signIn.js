function emptyForm(formE1, data, labels)
{
    for (let i = 0; i < labels.length; i++)
	{
        const value = data[labels[i]];
        if (!value || value.trim() === '')
		{
            printErrorMsg(formE1, { error: labels[i] + ' must not be empty' });
            return true;
        }
    }
    return false;
}

function	printErrorMsg(formE2, data)
{
	let msgFromBack = '';
	if (data.error)
		msgFromBack = data.error;
	else if (data.password)
		msgFromBack = data.password;
	else if (data.username)
		msgFromBack = data.username;
	else if (data.confirm_password)
		msgFromBack = data.confirm_password;
	else if (data.message)
		msgFromBack = data.message;
	else if (data.new_password)
		msgFromBack = data.new_password;
	const errorMsg = document.querySelector('#errorMsg')
	if (errorMsg)
		errorMsg.remove();
	const newErrorMsg=document.createElement('p')
	if (data.message)
	{
		newErrorMsg.style.color = 'green';
        newErrorMsg.style.border = '1px solid green';
        newErrorMsg.style.padding = '10px';
        newErrorMsg.style.marginTop = '10px';
        newErrorMsg.style.backgroundColor = '#e6ffe6';
	}
	else
	{
		newErrorMsg.style.color = 'red';
		newErrorMsg.style.border = '1px solid red';
		newErrorMsg.style.padding = '10px';
		newErrorMsg.style.marginTop = '10px';
		newErrorMsg.style.backgroundColor = '#ffe6e6';
	}
	newErrorMsg.id = 'errorMsg';
	newErrorMsg.textContent = msgFromBack;
	formE2.insertAdjacentElement('beforebegin', newErrorMsg);
}


const tfaLoginDiv = document.getElementById("tfaLoginDiv")
const tfaLogin = document.getElementById("tfaLogin")

function login()
{
	const formE1 = document.querySelector("form.signIn");
	formE1.addEventListener('submit', event => {
    	event.preventDefault();
        const formData = new FormData(formE1);
        var data = Object.fromEntries(formData);
		data.uid = tfaLoginDiv.getAttribute("uid")
        if (!emptyForm(formE1, data, ["username", "password"]))
		{
            fetch('/api/signIn', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(data)
            })
            .then(res => res.json())
            .then(responseData => {
				var id = undefined
				if (responseData.tfa) {
					tfaLoginDiv.style.display = "block"
					tfaLoginDiv.setAttribute("uid", responseData.tfa)
					let message = {"message" : "Check our mail and enter the code for connect"};
                    printErrorMsg(formE1, message);
					return
				}
            	else if (responseData.error) {
                    printErrorMsg(formE1, responseData);
                } else {
                    sessionStorage.setItem('userID', responseData.id);
					document.cookie = `userID=${responseData.id}`;
					changeDiv('accountDiv');
                }
            })
            .catch(error => {
                console.error('Error during fetch:', error);
                printErrorMsg(formE1, data);
            });
        }
    });
}

document.addEventListener('DOMContentLoaded', async function()
{
	if (!sessionStorage.getItem('userID'))
		await changeStatusRefresh();
	if (sessionStorage.getItem('userID') && findActiveDiv() === 'pongDiv')
	{
		await changeStatus();
	}
	page();
	if (!sessionStorage.getItem('userID'))
	{
		const div = findActiveDiv();
		if ( div === 'signUpDiv' || div === 'signInDiv' || div === 'homeDiv')
			{
				const userID = await getToken('userID');
				if (userID !== null)
				{
					sessionStorage.setItem('userID', userID);
					// await changeDiv('accountDiv');
				}
				// statusOfPlayer('accountDiv');
			}
	}
	let spinners = document.getElementById('spinners');
	if (spinners.style.display === 'none')
	{
		let homeDiv = document.getElementById('homeDiv');
		homeDiv.className = "container content";
		let noLogHome = document.getElementById('noLogHome');
		noLogHome.style.display = 'block';
	}
});

function loginVia42()
{
	// window.location.href = `https://api.intra.42.fr/oauth/authorize?client_id=u-s4t2ud-12af453a9b6e288fd49d5f5066c0cd575c0978d35fd6eb0c5be69b07d1ee993b&redirect_uri=https%3A%2F%2F${window.location.host}%3A1339%2Faccount&response_type=code`
	window.location.href = `https://api.intra.42.fr/oauth/authorize?client_id=u-s4t2ud-12af453a9b6e288fd49d5f5066c0cd575c0978d35fd6eb0c5be69b07d1ee993b&redirect_uri=https%3A%2F%2F10.33.3.4%3A1339%2Faccount&response_type=code`
}

document.getElementById('loginIntra').addEventListener('click', loginVia42);


function	page()
{
	login();
	signUp();
	logout();
	// addNotifBadge();
	tournamentForm();
	createJoinPage();
	// delog();
}
