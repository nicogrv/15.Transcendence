function getCSRFToken() {
	const cookieValue = document.cookie.match('(^|;)\\s*' + 'csrftoken' + '\\s*=\\s*([^;]+)');
	return cookieValue ? cookieValue.pop() : '';
}

let matchId = document.getElementById(`match`)
// var segments =  window.location.pathname.split('/');
// var lastSegment = segments[segments.length - 1];


async function createFlexDivBottom(content1, middleContent, content2, match)
{
    const flexDiv = document.createElement('div');
    flexDiv.style.cssText = 'display: flex; padding: 5px 10px; margin: 0px; width: 250px;';

    const h5_1 = document.createElement('h5');
    h5_1.style.cssText = 'margin: 0px; flex: 1; text-align: center; overflow: hidden; text-overflow: ellipsis;';
    h5_1.textContent = content1;

    if (middleContent === "playMatch") {
        var middleElem = document.createElement("button");
        middleElem.setAttribute("matchid", match.id);
        middleElem.innerText = "PLAY";
        middleElem.classList.add("btn", "btn-primary");
        middleElem.style.padding = "0px 5px 0px 5px";
        middleElem.style.cursor = 'pointer';
		middleElem.id = 'playButton';
		middleElem.onclick = async function()
		{
			await addDynamicStyles();
			startSocket(false);
			pongDiv('pongDiv', match.match.uid);
		};
		flexDiv.appendChild(h5_1);
    	flexDiv.appendChild(middleElem);
    } else {
        var middleElem = document.createElement('p');
        middleElem.style.cssText = 'margin: 0px 2px;';
        middleElem.textContent = middleContent;
		flexDiv.appendChild(h5_1);
    	flexDiv.appendChild(middleElem);
    }

    const h5_2 = document.createElement('h5');
    h5_2.style.cssText = 'margin: 0px; flex: 1; text-align: center; overflow: hidden; text-overflow: ellipsis;';
    h5_2.textContent = content2;

    // flexDiv.appendChild(h5_1);
    // flexDiv.appendChild(middleElem);
    flexDiv.appendChild(h5_2);
    return flexDiv;
}


async function displayMatch(match, status)
{
	const container = document.createElement('div');
	container.style.cssText = 'background-color: rgb(206, 206, 206); width: fit-content; border-radius: 6px;';

	const createFlexDivTop = (content1, middleContent, content2) => {
		const flexDiv = document.createElement('div');
		flexDiv.style.cssText = 'display: flex; padding: 5px 10px; margin: 0px; width: 250px;';
		const h5_1 = document.createElement('h5');
		h5_1.style.cssText = 'margin: 0px; flex: 1; text-align: center; overflow: hidden; text-overflow: ellipsis;';
		h5_1.textContent = match.player1;
		const p = document.createElement('p');
		p.style.cssText = 'margin: 0px 2px;';
		p.textContent = 'VS';
		const h5_2 = document.createElement('h5');
		h5_2.style.cssText = 'margin: 0px; flex: 1; text-align: center; overflow: hidden; text-overflow: ellipsis;';
		h5_2.textContent =  match.player2;


		flexDiv.append(h5_1, p, h5_2);

		return flexDiv;
	};

	const hr = document.createElement('hr');
    hr.style.margin = "2px";


	container.style.margin = "4px"
	container.append(createFlexDivTop(), hr);
	if (status == "end")
		container.append(await createFlexDivBottom((match.match.player1 == match.match.winner) ? "✅" : "❌", `${match.match.score_player1}-${match.match.score_player2}`, (match.match.player2 == match.match.winner) ? "✅" : "❌", match));
	else if (status === "status")
		container.append(await createFlexDivBottom("⌛", match.match.status, "⌛", match));
	else if (status == "playMatch")
		container.append(await createFlexDivBottom("⌛", "playMatch", "⌛", match));
	// playGame();
	matchId.appendChild(container);
	return container
}



function createDisplayWinner(match) {
	let divLevel = document.createElement("div")
	divLevel.id = `level_winner`
	let divLevelMatch = document.createElement("div")
	divLevelMatch.id = `level_winner_winner`
	divLevelMatch.style.display = "flex"
	let titleLevel = document.createElement("h4")
	titleLevel.innerText = `WINNER`
	divLevel.appendChild(titleLevel)
	divLevel.appendChild(divLevelMatch)
	matchId.appendChild(divLevel)
	const container = document.createElement('div');
	container.style.cssText = 'background-color: #FFD700; width: fit-content; border-radius: 6px;';
	const flexDiv = document.createElement('div');
	flexDiv.style.cssText = 'display: flex; padding: 5px 10px; margin: 0px; width: 250px;';
	const h5_1 = document.createElement('h5');
	h5_1.style.cssText = 'margin: 0px; flex: 1; text-align: center; overflow: hidden; text-overflow: ellipsis;';
	h5_1.textContent = "🏆🏆";
	var middleElem = document.createElement('h5');
	middleElem.style.cssText = 'margin: 0px 2px;';
	middleElem.textContent = match.match.winner;
	const h5_2 = document.createElement('h5');
	h5_2.style.cssText = 'margin: 0px; flex: 1; text-align: center; overflow: hidden; text-overflow: ellipsis;';
	h5_2.textContent =  "🏆🏆";
	flexDiv.append(h5_1, middleElem, h5_2);
	container.style.margin = "4px"
	container.append(flexDiv);
	divLevel.appendChild(container)
}

async function createDisplayMatch(match){
	var level = document.getElementById(`level_${match.level}`)
	if (!level) {
		let divLevel = document.createElement("div")
		divLevel.id = `level_${match.level}`
		let divLevelMatch = document.createElement("div")
		divLevelMatch.id = `level_${match.level}_match`
		divLevelMatch.style.display = "flex"
		let titleLevel = document.createElement("h4")
			if (match.level == 1)
				titleLevel.innerText = `FINAL`
			else
			titleLevel.innerText = `1/${match.level} final`
		divLevel.appendChild(titleLevel)
		divLevel.appendChild(divLevelMatch)
		matchId.appendChild(divLevel)
		level = divLevel
	}
	let divduel = document.getElementById(`level_${match.level}_match`)
	// divduel.innerHTML = '';
	if (match.hisMatch && match.match.status == "WAITPLAYERS")
		divduel.appendChild(await displayMatch(match, "playMatch"))
	else if (match.match.status == "WAITPLAYERS" || match.match.status == "GAMELAUNCH" || match.match.status == "INGAME")
		divduel.appendChild(await displayMatch(match, "status"))
	else if (match.match.status == "FINISH") {
		divduel.appendChild(await displayMatch(match, "end"))

	}
	return;
}

async function	addListPlayer(data)
{
	const playerInTournament = document.getElementById("playerInTournament")
	if (playerInTournament)
		playerInTournament.innerHTML = '';
	let i = 1;

	for (let index in data.players)
	{
		let elem = document.createElement('li');
		elem.classList.add('list-group-item');
		elem.style.backgroundColor = 'rgb(206, 206, 206)'
		elem.innerText = i + '. ' + data.players[index];
		i++;
		playerInTournament.appendChild(elem);

		// console.log(play);
	}

}


/*1er tableau*/
function	editTournamentFunction(tournamentId)
{
	const path = window.location.pathname.split('/');
	fetch(`/api/editTournament/` + tournamentId,{
		method: 'GET',
		headers: {
			'Content-Type': 'application/json',
			'X-CSRFToken': getCSRFToken(),
		}})
		.then(res => {
			return res.json();
		}).then(data => {
			// console.log(data)
			if ("error" in data) {
				changeDiv('tournamentDiv');
			}
			if ("ok" in data) {
				// console.log(data);
				data = data.ok
				document.getElementById("title").innerText = data.name
				document.getElementById("addonTitle").innerText = `${data.id}`
				document.getElementById("numberOfPlayer").innerText = `Player: ${data.numberOfPlayerNow}/${data.numberOfPlayer}`
				document.getElementById("password").innerText = `Password: ${data.password}`
				document.getElementById("admin").innerText = `Admin: ${data.admin}`

				let i = 0;
				matchId.innerHTML = '';
				addListPlayer(data);
				for (let index in data.match)
					{
						let match = data.match[i];
						i++;
						if (match.level == 1 && match.level == 1)
							createDisplayWinner(match)
					createDisplayMatch(match)
				}
				// console.log("couo")
				// if (data.status == "End") {

				// 	tsParticles.load('tsparticles', {
				// 		"fullScreen": {
				// 		  "zIndex": 1
				// 		},
				// 		"particles": {
				// 		  "color": {
				// 			"value": ["#ffaa00", "#ff0000", "#00ccff", "#55ff44", ]
				// 		  },
				// 		  "move": {
				// 			"direction": "bottom",
				// 			"enable": true,
				// 			"outModes": {
				// 			  "default": "out"
				// 			},
				// 			"size": true,
				// 			"speed": {
				// 			  "min": 1,
				// 			  "max": 1
				// 			}
				// 		  },
				// 		  "number": {
				// 			"value": 500,
				// 			"density": {
				// 			  "enable": true,
				// 			  "area": 800
				// 			}
				// 		  },
				// 		  "opacity": {
				// 			"value": 1,
				// 			"animation": {
				// 			  "enable": false,
				// 			  "startValue": "max",
				// 			  "destroy": "min",
				// 			  "speed": 0.3,
				// 			  "sync": true
				// 			}
				// 		  },
				// 		  "rotate": {
				// 			"value": {
				// 			  "min": 0,
				// 			  "max": 360
				// 			},
				// 			"direction": "random",
				// 			"move": true,
				// 			"animation": {
				// 			  "enable": true,
				// 			  "speed": 60
				// 			}
				// 		  },
				// 		  "tilt": {
				// 			"direction": "random",
				// 			"enable": true,
				// 			"move": true,
				// 			"value": {
				// 			  "min": 0,
				// 			  "max": 360
				// 			},
				// 			"animation": {
				// 			  "enable": true,
				// 			  "speed": 60
				// 			}
				// 		  },
				// 		  "shape": {
				// 			"type": ["circle", "square"],
				// 		  },
				// 		  "size": {
				// 			"value": {
				// 			  "min": 2,
				// 			  "max": 4
				// 			}
				// 		  },
				// 		  "roll": {
				// 			"darken": {
				// 			  "enable": true,
				// 			  "value": 30
				// 			},
				// 			"enlighten": {
				// 			  "enable": true,
				// 			  "value": 30
				// 			},
				// 			"enable": true,
				// 			"speed": {
				// 			  "min": 15,
				// 			  "max": 25
				// 			}
				// 		  },
				// 		  "wobble": {
				// 			"distance": 30,
				// 			"enable": true,
				// 			"move": true,
				// 			"speed": {
				// 			  "min": -15,
				// 			  "max": 15
				// 			}
				// 		  }
				// 		}
				// 	  });
				// }


				// console.log(listMatch)
			}
		})

}



async function addDynamicStyles()
{
    const style = document.createElement('style');
    style.innerHTML = `
        #tsparticles {
            position: absolute;
            width: 100%;
            height: 100%;
        }
    `;
    document.head.appendChild(style);
	return ;
}
