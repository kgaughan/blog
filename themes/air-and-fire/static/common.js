// Humanise any timestamps
window.addEventListener("DOMContentLoaded", () => {
	document.querySelectorAll("time").forEach((elem, _) => {
		if (elem.dateTime != "") {
			elem.innerText = dayjs(elem.dateTime).fromNow();
		}
	});
});
