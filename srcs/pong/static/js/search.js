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



//   var ctx = document.getElementById('myChart').getContext('2d');
//     var myChart = new Chart(ctx, {
//         type: 'line',
//         data: {
//             labels: "test",
//             datasets: [{
//                 label: 'Valeurs',
//                 data: {{ values|safe }},
//                 fill: false,
//                 borderColor: 'rgb(75, 192, 192)',
//                 tension: 0.1
//             }]
//         },
//         options: {
//             scales: {
//                 x: {
//                     type: 'time',
//                     time: {
//                         parser: 'YYYY-MM-DD HH:mm',
//                         tooltipFormat: 'll HH:mm',
//                         unit: 'hour',
//                         displayFormats: {
//                             hour: 'HH:mm'
//                         }
//                     },
//                     title: {
//                         display: true,
//                         text: 'Date et heure'
//                     }
//                 },
//                 y: {
//                     beginAtZero: true,
//                     title: {
//                         display: true,
//                         text: 'Valeurs'
//                     }
//                 }
//             }
//         }
//     });