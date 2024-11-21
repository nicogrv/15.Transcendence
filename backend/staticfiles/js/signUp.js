function signUp()
{
		const formE2 = document.querySelector("form.signUp");
		formE2.addEventListener('submit', event =>
		{
            event.preventDefault();
			const formData = new FormData(formE2);
			const data = Object.fromEntries(formData);
			data.username = data.username1;
			data.email = data.email1;
			data.password = data.password1;
			data.confirm_password = data.confirm_password1;
			if (emptyForm(formE2, data, ["username", "email", "password", "confirm_password"]))
				return ;
			else
			{
				fetch('/api/signUp', {
					method: 'POST',
					headers: {
						'Content-Type': 'application/json'
					},
					body:JSON.stringify(data)
				}).then(res => {
					return res.json();
				}).then(data => {
					if (data.error || data.password || data.username)
						printErrorMsg(formE2, data);
					else
					{
						sessionStorage.setItem('userID', 'connect');
						// document.cookie = `access=${data.access}; Secure; SameSite=Strict;`;
						// document.cookie = `refresh=${data.refresh}; Secure; SameSite=Strict;`;
						// statusChange(findActiveDiv(), 'accountDiv');
						changeDiv('accountDiv');
					}
				}).catch(error => {
					// console.log(error);
				})
			}
		})
	// }
}


