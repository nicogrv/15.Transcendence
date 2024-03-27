function changeColorMode(){
	let r = document.querySelector(':root');
	if (localStorage.getItem("day-night") == "day") {
		r.style.setProperty('--primary-color', '#dee2e6');
		r.style.setProperty('--seconde-color', '#adb5bd');
		r.style.setProperty('--text-color', '#232323');
		r.style.setProperty('--color-mode', 'day');
		localStorage.setItem("day-night", "day");
	}
	else {
		r.style.setProperty('--primary-color', '#0f0f0f');
		r.style.setProperty('--seconde-color', '#232323');
		r.style.setProperty('--text-color', '#dee2e6');
		r.style.setProperty('--color-mode', 'night');
		localStorage.setItem("day-night", "night");
	}
}

if (!localStorage.getItem("day-night"))
	localStorage.setItem("day-night", "day");
changeColorMode()
