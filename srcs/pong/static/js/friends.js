searchFriends = document.getElementById('searchFriends')
friends = document.getElementById('friends')

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

socketSession.addEventListener("message", (event) => {
	let newFriends = document.createElement("div");
	let jsonData = JSON.parse(event.data).usernameSearchValue
	if (jsonData) {
		for (let name in jsonData) {
			let elem = document.createElement("p");
			elem.style.border = "4px outset green";
			elem.style.background = "pink";
			elem.innerText = jsonData[name]
			console.log(`name ${jsonData[name]} ${elem}`)
			elem.addEventListener("click", (e) => {
				console.log(elem.innerText)
			})
			newFriends.appendChild(elem)
		}
		usernameFriends = document.getElementById('usernameFriends')
		newFriends.id = 'usernameFriends'
		friends.replaceChild(newFriends, usernameFriends)
		console.log("ici")
	}
	console.log("Message from server ", event.data);
  });