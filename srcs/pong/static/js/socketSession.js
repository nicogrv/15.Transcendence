function getCookie(name) {
    var cookies = document.cookie.split(';');
    for (var i = 0; i < cookies.length; i++) {
        var cookie = cookies[i].trim();
        if (cookie.indexOf(name + '=') === 0) {
            return cookie.substring(name.length + 1, cookie.length);
        }
    }
    return null;
}

let cookie = getCookie("PongToken");

const socketSession = new WebSocket(`ws://127.0.0.1:8000/socketSession/${cookie}`);

console.log('COUCOU')
socketSession.addEventListener("open", (event) => {
  socketSession.send(JSON.stringify("test"));
});

socketSession.addEventListener("message", (event) => {
  console.log("Message from server ", event.data);
});
