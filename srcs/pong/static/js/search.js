var searchFriends = document.getElementById('searchFriends')
var buttonBlock = document.getElementById("buttonBlock")
var buttonAddFriend = document.getElementById("buttonAddFriend")
var friends = document.getElementById('usernameFriends')
var updateRealtionName = null
var myModal = null
buttonAddFriend.addEventListener('click', updateRealtionFriends)
buttonBlock.addEventListener('click', updateRealtionBlock)


searchFriends.addEventListener('input', function(e) {
	if (this.value) {
		console.log(this.value)
		socketSession.send(JSON.stringify({"searchFriends" : this.value}));
	
	}
	else {
		let newFriends = document.createElement("div");
		newFriends.id = 'usernameFriendsDisplay'
		usernameFriendsDisplay = document.getElementById('usernameFriendsDisplay')
		friends.replaceChild(newFriends, usernameFriendsDisplay)
	}
})


function updateRealtionFriends() {
	if (!updateRealtionName)
		return
	fetch(`http://127.0.0.1:8000/api/user/updateRelation/?user=${updateRealtionName}&relation=friends`)
	.then(response => {
		if (!response.ok) {throw new Error('La requête a échoué');} return response.json(); })
	.then(data => {
		if ("ok" in data)
			modalClick()
	})
}

function updateRealtionBlock() {
	if (!updateRealtionName)
		return
	fetch(`http://127.0.0.1:8000/api/user/updateRelation/?user=${updateRealtionName}&relation=block`)
	.then(response => {
		if (!response.ok) {throw new Error('La requête a échoué');} return response.json(); })
	.then(data => {
		if ("ok" in data)
			modalClick()
	})
}



function modalClick() {
	fetch(`http://127.0.0.1:8000/api/user/getInfoPlayerOf/?username=${updateRealtionName}`)
	.then(response => {
		if (!response.ok) {throw new Error('La requête a échoué');} return response.json(); })
	.then(data => {
		document.getElementById("exampleModalLabel").innerText = data.username
		if (data.pic)
			document.getElementById("ppPlayerModal").setAttribute('src', data.pic) 
		else 
			document.getElementById("ppPlayerModal").setAttribute('src', "pong/static/img/poda.png") 
		document.getElementById('textModal').innerText = `${data.elo} Elo (${data.victories}/${data.defeats})
		Relation me to him: ${data.relationMeHim}
		Relation him to me: ${data.relationHimMe}
		`;
		myModal.show();
	})
}


socketSession.addEventListener("message", (event) => {
	let newFriends = document.createElement("div");
	let jsonData = JSON.parse(event.data).usernameSearchValue
	if (jsonData) {
		for (let name in jsonData) {
			let elem = document.createElement("p");
			elem.innerText = jsonData[name]
			elem.style.margin = "2px"
			console.log(`name ${jsonData[name]} ${elem}`)
			elem.addEventListener("click", (e) => {
				myModal = new bootstrap.Modal(document.getElementById('exampleModal'));
				updateRealtionName = jsonData[name] 
				modalClick()
			})
			let hr = document.createElement("hr")
			hr.style.margin = '4px'
			newFriends.appendChild(elem)
			newFriends.appendChild(hr)
		}
		usernameFriendsDisplay = document.getElementById('usernameFriendsDisplay')
		newFriends.id = 'usernameFriendsDisplay'
		let hr = document.createElement("hr")
		hr.style.margin = '4px'
		friends.replaceChild(newFriends, usernameFriendsDisplay)
	}
	console.log("Message from server ", event.data);
  });


  function padZero(num) {
	return (num < 10 ? '0' : '') + num;
  }
  function formatTimestamp(timestamp) {
	var dt_object = new Date(timestamp);
	var time_sec = padZero(dt_object.getUTCSeconds());
	var time_hour = padZero(dt_object.getUTCHours());
	var time_minute = padZero(dt_object.getUTCMinutes());
	var date_day = padZero(dt_object.getUTCDate());
	var date_month = padZero(dt_object.getUTCMonth() + 1);
	var date_year = padZero(dt_object.getUTCFullYear() % 100); 
	return time_hour + ":" + time_minute + ":" + time_sec + " " + date_day + "/" + date_month + "/" + date_year;
  }



function makePointShart(Title, Color, TextY, apiUrl, canva, snowBallData) {
	fetch(`${window.location.origin}${apiUrl}`)
	.then(response => {
		if (!response.ok) {throw new Error('La requête a échoué');} return response.json(); })
	.then(data => {
		var labels = [];
		var values = [];
		data.ok.forEach(function(item) {
			var timestamp = Object.keys(item)[0];
			var value = item[timestamp];
			timestamp = formatTimestamp(timestamp)
			if (!labels.includes(timestamp)) {
				labels.push(timestamp);
				console.log(value, timestamp)
				if (values.length > 0 && snowBallData)
					values.push(parseInt(values[values.length -1]) + parseInt(value))
				else 
					values.push(parseInt(value))
			}
		});
		new Chart(canva, {
			type: 'line',
			data: {
				labels: labels,
				datasets: [{
					label: Title,
					data: values,
					fill: true,
					borderColor: Color,
					tension: 0
				}]
			},
			options: {
				responsive: false,
				scales: {
					x: {
						title: {
							display: true,
							text: 'Date'
						}
					},
					y: {
						beginAtZero: true,
						title: {
							display: true,
							text: TextY
						}
					}
				}
			}
		});
	})
}

makePointShart('Point in game', 'rgb(255, 255, 255)', "Point",  "/api/user/getPointWithDate", document.getElementById('pointChart').getContext('2d'), true)
makePointShart('Elo', 'rgb(255, 255, 255)', "Elo",  "/api/user/getEloWithDate", document.getElementById('eloChart').getContext('2d'), false)