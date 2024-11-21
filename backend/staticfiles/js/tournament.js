function getCSRFToken() {
    const cookieValue = document.cookie.match('(^|;)\\s*' + 'csrftoken' + '\\s*=\\s*([^;]+)');
    return cookieValue ? cookieValue.pop() : '';
}

function getAliasByUserId(players, userId) {
    const player = players.find(player => player.id === userId);
    return player ? player.name : null;
}

var dataMatch
function createJoinMatch(data, progress) {
    var mainDiv = document.createElement('div');
	mainDiv.className = 'col-12 col-md-6 col-lg-4';
    mainDiv.style.backgroundColor = '#b4b4b4';
    mainDiv.style.padding = '10px';
    mainDiv.style.margin = '4px';
    mainDiv.style.borderRadius = '20px';
    mainDiv.style.width = '250px';
    var nameHeader = document.createElement('h3');
	nameHeader.textContent = data.name;
    mainDiv.appendChild(nameHeader);

    var idParagraph = document.createElement('p');
    idParagraph.textContent = data.id;
	idParagraph.className = 'text-truncate';
    mainDiv.appendChild(idParagraph);

	var registred = document.createElement('p');
	registred.style.fontWeight = 'bold';
	registred.className = 'text-truncate';
	if (progress === 'progress')
		registred.textContent = 'REGISTERED'
	else
		registred.textContent = 'WAITING PLAYER(S)'
	mainDiv.appendChild(registred);

    var playerParagraph = document.createElement('p');
    playerParagraph.textContent = `Player: ${data.numberOfPlayerNow}/${data.numberOfPlayer}`;
    mainDiv.appendChild(playerParagraph);

    var buttonDiv = document.createElement('div');
    buttonDiv.style.margin = '0px 5px 5px 5px';

    var joinButton = document.createElement('button');
    joinButton.type = 'button';
	if (progress !== 'progress')
    	joinButton.className = 'btn btn-primary';

    joinButton.style.width = '100%';
    joinButton.textContent = 'Join tournament';
    joinButton.addEventListener("click", e =>
	{
		console.log("clickkkkkkk")
        dataMatch = data;
		const alias = document.getElementById('aliasModal');
		const aliasName = getAliasByUserId(data.players, sessionStorage.getItem('userID'));
		const printAlias = document.getElementById('aliasPrint')
		if (aliasName)
		{
			printAlias.innerHTML = 'Your alias : ' + aliasName;
			alias.style.display = "none";
			printAlias.style.display = 'block';
		}
		else
		{
			printAlias.style.display = 'none';
			alias.style.display = "block";
		}
        if (data.password == "True") {
            document.getElementById("passswordModal").style.display = "block"
            document.getElementById("passswordModalInput").value = ""
        }
        else
            document.getElementById("passswordModal").style.display = "none"
        e.preventDefault();
        myModal.show();
		modal(myModal);
        // $('#staticBackdrop').modal('show');
    })

    buttonDiv.appendChild(joinButton);
    mainDiv.appendChild(buttonDiv);
    document.getElementById("listMatch").appendChild(mainDiv);
}


const tournamentHistory = document.getElementById('tournamentHistory')

function createDropdownItem(tournament) {
	console.log(tournament)
    const li = document.createElement('li');
    li.innerHTML = `<a class="dropdown-item" href="/tournament/${tournament.id}">${tournament.name}</a>`;
	console.log(li)
	console.log(tournamentHistory)
    tournamentHistory.appendChild(li)

}



async function getTournamentList() {
    fetch(`${window.location.origin}/api/getTournamentAvailable`,{
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCSRFToken(),
        },
    }).then(res => {
        return res.json();
    }).then(data => {
        console.log(data)
        if ("error" in data)
            console.error(data)
        if ("ok" in data) {
			console.log(data);
            data = data.ok
			let div = document.getElementById("listMatch");
			if (div)
				div.innerHTML = '';
            for(index in data.waiting) {
                createJoinMatch(data.waiting[index], 'waiting');

            }
        }
    })
}

function	tournamentForm()
{
	const formE1 = document.querySelector("form.createTournamentForm");
	formE1.addEventListener('submit', event => {
    	event.preventDefault();

		var checkedPassword = document.getElementById("switchPasswordCheckbox")
		createJoinPage();
		const dataForm = new FormData(document.getElementById("createTournamentForm"));
		var json =  JSON.stringify(Object.fromEntries(dataForm));
		let jsonParse = JSON.parse(json);
	if (!jsonParse.tournamentName || !jsonParse.alias || jsonParse.numberOfPlayers == "-" || (checkedPassword.checked && (!jsonParse.password || !jsonParse.confirmPassword))) {
		document.getElementById("liveToastMessage").textContent = "Error: Fields are incomplete !"
		bootstrap.Toast.getOrCreateInstance(document.getElementById('liveToast')).show()
		return ;
	}
	else if (jsonParse.password != jsonParse.confirmPassword) {
		document.getElementById("liveToastMessage").textContent = "Error: Passwords are not identical !"
		bootstrap.Toast.getOrCreateInstance(document.getElementById('liveToast')).show()
		return ;
	}
	else {
		fetch(`${window.location.origin}/api/createTournament`,{
			method: 'POST',
			headers: {
				'Content-Type': 'application/json',
				'X-CSRFToken': getCSRFToken(),
			},
			body:json
		}).then(res => {
			return res.json();
		}).then(data => {
			if ("error" in data) {
				console.error(data)
			}
			if ("ok" in data) {
				getTournamentList();
				editTournamentFunction(data.ok);
				tournamentDiv('tournamentEditDiv', data.ok);
			}
		})
	}
});
}
async function tournamentDiv(divTo, tournamentId)
{
    try {
        const div = document.getElementById(findActiveDiv());
        const divTarget = document.getElementById(divTo);

		div.style.display = 'none';
        divTarget.style.display = 'grid';
        changeNav(divTo);

        const addUrl = divTo.replace('EditDiv', '');
        if (addUrl !== 'home')
            window.history.pushState(divTo, 'title', '/' + addUrl + '/'+ tournamentId);
		// alreadyTournament();
		editTournamentFunction(tournamentId);
		statusOfPlayer(divTo);
    } catch (error) {
        console.error('Error in EditDiv:', error);
    }
}

function pongDiv(divTo, tournamentId)
{
    try {
        const div = document.getElementById(findActiveDiv());
        const divTarget = document.getElementById(divTo);

		div.style.display = 'none';
        divTarget.style.display = 'grid';
        changeNav(divTo);

        const addUrl = divTo.replace('Div', '');

        if (addUrl !== 'home')
            window.history.pushState(addUrl + 'Div', 'title', '/' + addUrl + '?id=' + tournamentId);
    } catch (error) {
        // console.error('Error in Div:', error);
    }
}
/*pour password du form*/
function createJoinPage() {
    var checkedPassword = document.getElementById("switchPasswordCheckbox")
    checkedPassword.addEventListener("change", function() {
        if (this.checked) {
            document.getElementById("divCreatePassword").style.display = "block";
            document.getElementById("divCreateConfirmPassword").style.display = "block";
        } else {
            document.getElementById("divCreatePassword").style.display = "none";
            document.getElementById("divCreateConfirmPassword").style.display = "none";
        }
    });
}


async function alreadyTournament()
{
	fetch(`/api/alreadyInTournament`,{
		    method: 'GET',
		    headers: {
		        'Content-Type': 'application/json',
		        'X-CSRFToken': getCSRFToken(),
		    },
		}).then(res => {
		    return res.json();
		}).then(data => {
		    // if ("error" in data) {
		    //     // console.error(data)
		    // }
		    if ("tournament" in data)
			{
		        if (data.tournament == "no")
				{
		            createJoinPage()
					getTournamentList();
					// editTournamentFunction();
		    	}
		    	else
				{
					tournamentDiv('tournamentEditDiv',data.tournament);
		        	// document.location = `tournament/${data.tournament}`
		    	}

	    	}
		getTournamentHistory()
	})
}

var myModal = new bootstrap.Modal(document.getElementById('staticBackdrop'));
document.getElementById("enterInTournament").addEventListener("click", e => {
	e.preventDefault()
	console.log("click enterInTournament")
	let aliasValue = document.getElementById("aliasForTournament");
	const aliasModal = document.getElementById('aliasModal');
	let password = undefined
	if (window.getComputedStyle(aliasModal).display !== 'none' && !aliasValue.value) {
		document.getElementById("liveToastMessage").textContent = "Error: Alias fields are incomplete !"
		bootstrap.Toast.getOrCreateInstance(document.getElementById('liveToast')).show()
		return;
	}
	else if (dataMatch.password == "True") {
		password = document.getElementById("passswordModalInput").value
	}
	console.log("bonjour je fetch")
	fetch(`${window.location.origin}/api/joinTournament`,{
		method: 'POST',
		headers: {
			'Content-Type': 'application/json',
			'X-CSRFToken': getCSRFToken(),
		},
		body:JSON.stringify({"id":dataMatch.id, "alias": aliasValue.value, "password":password})
		}).then(res => {
			return res.json();
		}).then(data => {
			if ("error" in data) {
				// myModal.hide();
				document.getElementById("liveToastMessage").textContent = `Error: ${data.error} !`
				bootstrap.Toast.getOrCreateInstance(document.getElementById('liveToast')).show()
			}
			if ("ok" in data) {
				// var myModal = new bootstrap.Modal(document.getElementById('staticBackdrop'));
				myModal.hide();
				editTournamentFunction(dataMatch.id);
				tournamentDiv('tournamentEditDiv', dataMatch.id);
			}
		})
	// console.log(dataMatch.id, dataMatch.name)
})

/*aller dans un tournament qui existe*/
function	modal(myModal)
{
	document.getElementById("enterInTournament").addEventListener("click", e => {
		e.preventDefault();
		myModal.hide();
		return ;
	})
}

function getTournamentHistory(){
    fetch(`${window.location.origin}/api/getUserTournament`,{
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCSRFToken(),
        },
    }).then(res => {
        return res.json();
    }).then(data => {
        console.log(data)
        if ("error" in data)
            console.error(data)
        if ("ok" in data) {
            data = data.ok
            for(index in data) {
                createDropdownItem(data[index])
            }
        }
    })
}
