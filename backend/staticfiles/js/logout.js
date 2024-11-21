function deleteCookie(name) {
    var cookieArray = document.cookie.split("; ");
    for(var i = 0; i < cookieArray.length; i++) {
        var cookiePair = cookieArray[i].split("=");
        var cookieName = cookiePair[0];
        var cookieValue = cookiePair[1];
        if(name === cookieName) {
            document.cookie = name + "=;expires=Thu, 01 Jan 1970 00:00:00 GMT;path=/;";
            if (cookieValue.includes('.')) {
                var domainParts = cookieValue.split('.');
                var domain = '.' + domainParts.slice(domainParts.length - 2).join('.') + ';';
                document.cookie = name + "=;expires=Thu, 01 Jan 1970 00:00:00 GMT;path=/;" + domain;
            }
            break;
        }
    }
}

function	backLogout()
{
	const csrftoken = getToken('csrftoken');

            fetch('/api/playerLogout', {
                method: 'POST',
                headers: {
					'X-CSRFToken': csrftoken,
                    'Content-Type': 'application/json'
                }
            })
            .then(async response => {
                // if (response.ok) {

                sessionStorage.removeItem('userID');
                deleteCookie('access');
                deleteCookie('refresh');
                deleteCookie('userID');
                await changeDiv('homeDiv');
                window.location.reload();
                disconnectWebsocket();
                // } else {
                    // console.error('Logout failed:', response.statusText);
                // }
            })
            .catch(error => {
            });
}


function logout()
{

	const logoutButton = document.getElementById('logout');
	if (logoutButton)
	{
		logoutButton.addEventListener('click', function(event) {
		// event.preventDefault();

			if (!sessionStorage.getItem('userID'))
			{
				clearInput();
				changeDiv('signInDiv');
			}
			else
			{
				backLogout();
			}
		});
	}
}

function getToken(cookieName)
{
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++)
	{
        const cookie = cookies[i].trim();
        if (cookie.startsWith(cookieName + '='))
		{
            return cookie.substring(cookieName.length + 1);
        }
    }
    return null;
}

