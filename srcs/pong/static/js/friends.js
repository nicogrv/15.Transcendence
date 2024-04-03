var searchFriends = document.getElementById('searchFriends')
var friends = document.getElementById('friends')
var buttonBlock = document.getElementById("buttonBlock")
var buttonAddFriend = document.getElementById("buttonAddFriend")
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
		newFriends.id = 'usernameFriends'
		usernameFriends = document.getElementById('usernameFriends')
		friends.replaceChild(newFriends, usernameFriends)
	}
})


function updateRealtionFriends() {
	if (!updateRealtionName)
		return
	console.log("1 OK reload")
	fetch(`${window.location.origin}/api/user/updateRelation/?user=${updateRealtionName}&relation=friends`)
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
	fetch(`${window.location.origin}/api/user/updateRelation/?user=${updateRealtionName}&relation=block`)
	.then(response => {
		if (!response.ok) {throw new Error('La requête a échoué');} return response.json(); })
	.then(data => {
		if ("ok" in data)
			modalClick()
	})
}


function modalClick() {
	fetch(`${window.location.origin}/api/user/getInfoPlayerOf/?username=${updateRealtionName}`)
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
			elem.style.border = "1px outset green";
			elem.style.background = "pink";
			elem.innerText = jsonData[name]
			console.log(`name ${jsonData[name]} ${elem}`)
			elem.addEventListener("click", (e) => {
				myModal = new bootstrap.Modal(document.getElementById('exampleModal'));
				updateRealtionName = jsonData[name] 
				modalClick()
			})
			newFriends.appendChild(elem)
		}
		usernameFriends = document.getElementById('usernameFriends')
		newFriends.id = 'usernameFriends'
		friends.replaceChild(newFriends, usernameFriends)
	}
	console.log("Message from server ", event.data);
  });