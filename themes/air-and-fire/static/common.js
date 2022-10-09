// Humanise any timestamps
window.addEventListener("DOMContentLoaded", () => {
	let humanise = (dt) => luxon.DateTime.fromISO(dt).toRelative();
	document.querySelectorAll("time").forEach((elem, _) => {
		if (elem.dateTime != "") {
			elem.innerText = humanise(elem.dateTime);
		}
	});
});
