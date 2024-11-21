async function getTournamentMatches(tournamentId) {
    try {
        const response = await fetch(`/api/tournament/${tournamentId}/editTournament`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            'X-CSRFToken': getCSRFToken(),
            }
        });

        if (!response.ok) {
            throw new Error(`Erreur: ${response.statusText}`);
        }

        const data = await response.json();
        if (data.ok) {
            return (data)
        }
		// else {
        //     console.error("Erreur dans les données reçues: ", data.error);
        // }
    } catch (error) {
        // console.error("Erreur lors de la récupération des matchs du tournoi: ", error);
    }
}

// notifications
var loc = window.location
	var wsStart = "ws://"
	if (loc.protocol == "https:") {
		wsStart = "wss://"
	}

	var webSocketEndpoint = wsStart + loc.host + `/notify/`;

	let notifySocket;

	async function connectWebSocket()
	{
		while (!isUserLoggedIn()) {
			await new Promise(resolve => setTimeout(resolve, 500));
		}

		notifySocket = new WebSocket(webSocketEndpoint);

		notifySocket.onopen = function() {
			// console.log('WebSocket connection established');
		};

		let isProcessing = false;

		notifySocket.onclose = function(event) {
			if (!event.wasClean || event.code !== 1000 || event.code == 1006) {
				console.log('Websocket connection closed uncleanly')
			} else {
				console.log('Websocket connection closed cleanly');
			}
		};

		notifySocket.onerror = function(error) {
			// console.error('Websocket error:', error);
			notifySocket.close();
		};

		notifySocket.onmessage = function(event)
		{
			try {
				var data = JSON.parse(event.data);
				if (data.type === 'notification') {
					setMessage(data, data.id,);
				} else if (data.type === 'friend_request_deleted') {
					removeNotif(data.notif_id);
				} else if (data.type === 'player_joined_tournament') {
                    const activeDiv = window.location.pathname;
                    if (activeDiv === '/tournament/' + data.tournois_id)
                    {
                        if (!isProcessing) {
                            isProcessing = true;

                            editTournamentFunction(data.tournois_id);
                            tournamentDiv('tournamentEditDiv', data.tournois_id);

                            setTimeout(() => {
                                isProcessing = false;
                            }, 1000);
                        }
                    }

                } else if (data.type === 'player_left_tournament') {


                } else if (data.type === 'match_end') {

                }
			} catch (error) {
			}
		};
	}

	window.onload = function() {
		connectWebSocket();
	};

	function disconnectWebsocket() {
		if (notifySocket) {
			notifySocket.close();
		}
	}

	function isUserLoggedIn() {
		const userId = sessionStorage.getItem("userID");
		if (userId) {
			return true;
		}
		return false;
	}
