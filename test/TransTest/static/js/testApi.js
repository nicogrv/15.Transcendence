var app = document.getElementById("app")

function updateUserPage(user, id) {

	var form = document.createElement("form")
	var input = document.createElement("input")
	form.appendChild(input);
	form.addEventListener('submit', function(e) {
		e.preventDefault();
		console.log("OK")
		if (id == "Name") {

			fetch(`/blog/api/UpdateUser/${user.fields.uid}/Name/${input.value}`)
			.then(response => {if (!response.ok) {throw new Error('La requête a échoué');}return response.json(); })
			.then(data => {console.log(data)})
		}
		else if (id == "Age") {
			fetch(`/blog/api/UpdateUser/${user.fields.uid}/Age/${input.value}`)
			.then(response => {if (!response.ok) {throw new Error('La requête a échoué');}return response.json(); })
			.then(data => {console.log(data)})
		}
	})
	return form
}

async function addUserPage(user) {
	var div = document.createElement("div")
	var divName = document.createElement("div")
	var divAge = document.createElement("div")
	divName.style.display = "flex"	
	divAge.style.display = "flex"	
	// div.style.marginBottom = "500px"
	div.style.backgroundColor = "#dee2e6"
	var titre = document.createElement("h3")
	var age = document.createElement("p")
	titre.innerHTML = `${user.pk} Name: ${user.fields.Name}`;
	age.innerHTML = `Age: ${user.fields.Age}`
	divName.appendChild(titre)
	divName.appendChild(updateUserPage(user, "Name"))
	divAge.appendChild(age)
	divAge.appendChild(updateUserPage(user, "Age"))
	div.setAttribute("idUser", user.pk)
	app.appendChild(divName)
	app.appendChild(divAge)
}

function printUser() {

	fetch("/blog/api/getUser")
	.then(response => {
		if (!response.ok) {throw new Error('La requête a échoué');}
		return response.json(); 
	})
	.then(data => {
		data = JSON.parse(data.json)
		console.log(data);
		for (i in data)
		{
			// console.log(i);
			addUserPage(data[i])
			console.log(i, data[i].fields.Name);
		}
	})
}

try
{
	printUser();
} catch (e)
{
	console.log(e);
}