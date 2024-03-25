searchFriends = document.getElementById('searchFriends')
friends = document.getElementById('friends')
buttonBlock = document.getElementById("buttonBlock")
buttonAddFriend = document.getElementById("buttonAddFriend")




searchFriends.addEventListener('input', function(e) {
	if (this.value) {
		console.log(this.value)
		socketSession.send(JSON.stringify({"searchFriends" : this.value}));
	
	}
	else {
		let newFriends = document.createElement("div");
		newFriends.id = 'usernameFriends'
		usernameFriends = document.getElementById('usernameFriends')
		friends.replaceChild(newFriends, usernameFriends)
	}
})


function updateRealtion(name, relation) {
		fetch(`http://127.0.0.1:8000/api/user/updateRelation/?user=${name}&relation=${relation}`)
		.then(response => {
			if (!response.ok) {throw new Error('La requête a échoué');} return response.json(); })
		.then(data => {
			if ("ok" in data)
			buttonBlock.removeEventListener('click', updateRealtion);
			buttonAddFriend.removeEventListener('click', updateRealtion);
			modalClick(name)
		})
}


function modalClick(name) {
	fetch(`http://127.0.0.1:8000/api/user/getInfoPlayerOf/?username=${name}`)
	.then(response => {
		if (!response.ok) {throw new Error('La requête a échoué');} return response.json(); })
	.then(data => {
		document.getElementById("exampleModalLabel").innerText = data.username
		if (data.pic)
			document.getElementById("ppPlayerModal").setAttribute('src', data.pic) 
		else 
			document.getElementById("ppPlayerModal").setAttribute('src', "pong/static/img/poda.png") 
		document.getElementById('textModal').innerText = `
		${data.elo} Elo (${data.victories}/${data.defeats})
		Relation me to him: ${data.relationMeHim}
		Relation him to me: ${data.relationHimMe}
		`;
		buttonBlock.addEventListener('click', function() {
			console.log(name, "block")
			updateRealtion(name, "block");
		});
		buttonAddFriend.addEventListener('click', function() {
			console.log(name, "friends")
			updateRealtion(name, "friends");
		});
	})
}


socketSession.addEventListener("message", (event) => {
	let newFriends = document.createElement("div");
	let jsonData = JSON.parse(event.data).usernameSearchValue
	if (jsonData) {
		for (let name in jsonData) {
			let elem = document.createElement("p");
			elem.style.border = "1px outset green";
			elem.style.background = "pink";
			elem.innerText = jsonData[name]
			console.log(`name ${jsonData[name]} ${elem}`)
			elem.addEventListener("click", (e) => {
				var myModal = new bootstrap.Modal(document.getElementById('exampleModal'));
				myModal.show();
				modalClick(jsonData[name])
			})
			newFriends.appendChild(elem)
		}
		usernameFriends = document.getElementById('usernameFriends')
		newFriends.id = 'usernameFriends'
		friends.replaceChild(newFriends, usernameFriends)
	}
	console.log("Message from server ", event.data);
  });