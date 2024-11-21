function displayResults(data, id)
{
    var resultsDiv = document.getElementById(id);
    resultsDiv.innerHTML = '';

    if ('message' in data) {
        resultsDiv.innerHTML = '0 results';
        return ;
    }
    const usernameList = document.createElement('div');
    usernameList.style.display = 'flex';
    usernameList.style.flexWrap = 'wrap';
    usernameList.style.justifyContent = 'center';
// const dataResult = data.accounts;
    data.accounts.forEach(function(i)
    {
        let friendItem = document.createElement('div');
        friendItem.style.display = 'flex';
        friendItem.style.flexDirection = 'column';
        friendItem.style.alignItems = 'center';
        friendItem.style.margin = '10px';
        friendItem.style.padding = '10px';
        friendItem.style.border = '1px solid #ccc';
        friendItem.style.borderRadius = '10px';
        friendItem.style.width = '50%';
        friendItem.style.maxWidth = '250px';

        const avatar = document.createElement('img');
        if (i.avatar.includes(PATH_AVATAR_BACKEND))
			avatar.src = `${url}${i.avatar}`;
		else
			avatar.src = i.avatar;

        avatar.alt = `${i.username}'s avatar`;
        avatar.style.width = '100%';
        avatar.style.height = '100%';
        avatar.style.borderRadius = '50%';
        avatar.style.cursor = 'pointer';
        if (i.status_profile_str === "Offline")
            avatar.style.border = '4px solid grey';
        else if (i.status_profile_str === "Online")
            avatar.style.border = '4px solid green';
        else
            avatar.style.border = '4px solid orange';
            avatar.onclick = function() {
                userProfile(i.username);
            };

            const friendName = document.createElement('p');
            friendName.textContent = i.username;
            friendName.style.color = 'black';
            friendName.style.textAlign = 'center';
            friendName.style.fontWeight = 'bold';
            friendName.style.fontSize = 'large';
            friendName.style.margin = '10px 0 5px 0';
            friendName.style.cursor = 'pointer';
            friendName.onclick = function() {
                userProfile(i.username);
            };

        var relation = document.createElement('button');
        relation.style.color = 'white';
        if (i.is_friend)
        {
            relation.innerHTML = '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-arrow-through-heart" viewBox="0 0 16 16"> <path fill-rule="evenodd" d="M2.854 15.854A.5.5 0 0 1 2 15.5V14H.5a.5.5 0 0 1-.354-.854l1.5-1.5A.5.5 0 0 1 2 11.5h1.793l.53-.53c-.771-.802-1.328-1.58-1.704-2.32-.798-1.575-.775-2.996-.213-4.092C3.426 2.565 6.18 1.809 8 3.233c1.25-.98 2.944-.928 4.212-.152L13.292 2 12.147.854A.5.5 0 0 1 12.5 0h3a.5.5 0 0 1 .5.5v3a.5.5 0 0 1-.854.354L14 2.707l-1.006 1.006c.236.248.44.531.6.845.562 1.096.585 2.517-.213 4.092-.793 1.563-2.395 3.288-5.105 5.08L8 13.912l-.276-.182a22 22 0 0 1-2.685-2.062l-.539.54V14a.5.5 0 0 1-.146.354zm2.893-4.894A20.4 20.4 0 0 0 8 12.71c2.456-1.666 3.827-3.207 4.489-4.512.679-1.34.607-2.42.215-3.185-.817-1.595-3.087-2.054-4.346-.761L8 4.62l-.358-.368c-1.259-1.293-3.53-.834-4.346.761-.392.766-.464 1.845.215 3.185.323.636.815 1.33 1.519 2.065l1.866-1.867a.5.5 0 1 1 .708.708z"/> </svg> Friends';
            relation.style.backgroundColor = 'green';
        }
        else if (i.is_self === true)
        {
            relation.textContent = 'You';
            relation.style.backgroundColor = 'mediumorchid';
        }
        else
        {
            relation.innerHTML = '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-outlet" viewBox="0 0 16 16"> <path d="M3.34 2.994c.275-.338.68-.494 1.074-.494h7.172c.393 0 .798.156 1.074.494.578.708 1.84 2.534 1.84 5.006s-1.262 4.297-1.84 5.006c-.276.338-.68.494-1.074.494H4.414c-.394 0-.799-.156-1.074-.494C2.762 12.297 1.5 10.472 1.5 8s1.262-4.297 1.84-5.006m1.074.506a.38.38 0 0 0-.299.126C3.599 4.259 2.5 5.863 2.5 8s1.099 3.74 1.615 4.374c.06.073.163.126.3.126h7.17c.137 0 .24-.053.3-.126.516-.633 1.615-2.237 1.615-4.374s-1.099-3.74-1.615-4.374a.38.38 0 0 0-.3-.126h-7.17z"/> <path d="M6 5.5a.5.5 0 0 1 .5.5v1.5a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5m4 0a.5.5 0 0 1 .5.5v1.5a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5M7 10v1h2v-1a1 1 0 0 0-2 0"/></svg> Not Friends';
            relation.style.backgroundColor = 'silver';
        }
        friendItem.appendChild(avatar);
        friendItem.appendChild(friendName);
        friendItem.appendChild(relation);
        usernameList.appendChild(friendItem);
    });
    resultsDiv.appendChild(usernameList);
}


function searchPlayers(elementId)
{
    // clearInput();
    var query = document.getElementById(elementId).value;
    document.getElementById('searchQuery1').value = '';
    document.getElementById('searchQuery').value = '';
    const csrftoken = getToken('csrftoken');
    if (query) {
        fetch(`/api/search?query=${query}`, {
            method: 'GET',
            headers: {
                'X-CSRFToken': csrftoken,
                'Content-Type': 'application/json',
            },
        })
            .then(response => {
                return response.json();
            })
            .then(data => {
                // if (!data.message)
                displayResults(data, 'results');
                changeDiv('searchDiv')
            })
            .catch(error => {
                console.error('There was a problem with the fetch operation:', error);
            });
    } else {
        var resultsDiv = document.getElementById('results');
        resultsDiv.innerHTML = '';
        resultsDiv.innerHTML = '0 results';
        changeDiv('searchDiv');
    }
}