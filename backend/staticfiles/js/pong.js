const canvas = document.getElementById('pongCanvas');
const ctx = canvas.getContext('2d');
var token
var socket;
var pong
var socketJsonGame = null;
var socketJsonPoint
var socketJsonParticle = "";
var socketJsonStartTimming = "Waiting player ...";
var sendData = true
var updatePaddelAndBall = false
var newGame = false
window.addEventListener('resize', function(){
	sizeMultiplier = calculateInvertedMultiplier();
    updatePaddelAndBall = true
})

function calculateInvertedMultiplier() {
    const canvasWidth = 800;
    const canvasHeight = 600;
    const windowWidth = window.innerWidth - 50;
    const windowHeight = window.innerHeight - 130;
    const widthMultiplier = canvasWidth / windowWidth;
    const heightMultiplier = canvasHeight / windowHeight;
    const multiplier = Math.max(widthMultiplier, heightMultiplier);
    canvas.width = canvasWidth / multiplier
	canvas.height = canvasHeight / multiplier
    return multiplier;
}
var sizeMultiplier = calculateInvertedMultiplier();

class Pong {
    constructor(leftColor, rightColor, ballColor, speedPadle, speedBall) {
        var rPad = new Paddle("right", rightColor);
        var lPad = new Paddle("left", leftColor);
        var ball = new Ball(ballColor);
        this.rightColor = rightColor
        this.leftColor = leftColor
        this.ballColor = ballColor
        this.ballColor = ballColor
        this.playerNb = 0
        this.startGame = false;
        this.lPoint = 0
        this.rPoint = 0
        this.beforeGame = true
        this.beforeGameIndex = 0
        this.beforeGameMsg = []
        this.stopGame = false
        this.updateStat = true;
        rPad.s = speedPadle
        lPad.s = speedPadle
        ball.s = speedBall
        ctx.fillStyle = '#0f0f0f';
        ctx.fillRect(0, 0, canvas.width, canvas.height);
        this.gameLoop(0, lPad, rPad, ball);
    }

    beforeGameLoop() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        ctx.fillStyle = 'black';
        ctx.fillRect(0, 0, canvas.width, canvas.height);
        ctx.fillStyle = "#fff";
        ctx.font = '20px Arial';
        ctx.textBaseline = 'middle'
        ctx.textAlign = 'start';
        let beforeGameIndex = 20
        for (let text in this.beforeGameMsg) {
            ctx.fillText(this.beforeGameMsg[text], 20, beforeGameIndex);
            beforeGameIndex += 20
        }
    }

    draw(lPad, rPad, ball, frame) {
        // clear screen
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        // color background
        ctx.fillStyle = '#0f0f0f';
        ctx.fillRect(0, 0, canvas.width, canvas.height);
        // display point
        ctx.font = `${124/sizeMultiplier}px Arial`;
        ctx.textAlign = 'center';
        ctx.textBaseline = 'middle';
        ctx.fillStyle = lPad.color;
        ctx.fillText(this.lPoint, canvas.width/2/2, 100/sizeMultiplier);
        ctx.fillStyle = rPad.color;
        ctx.fillText(this.rPoint, canvas.width/2 + (canvas.width/2/2), 100/sizeMultiplier);
        // fill pad
        ctx.fillStyle = lPad.color;
        if (!this.startGame && frame/50%1 > 0.5 && this.playerNb == 1)
            ctx.fillStyle = '#0f0f0f';

        ctx.fillRect(lPad.x, lPad.y, lPad.w, lPad.h);
        ctx.fillStyle = rPad.color;
        if (!this.startGame && frame/50%1 > 0.5 && this.playerNb == 2)
            ctx.fillStyle = '#0f0f0f';
        ctx.fillRect(rPad.x, rPad.y, rPad.w, rPad.h);
        // animateParticles
        ball.animateParticles(ctx)
        // display ball
        ctx.fillStyle = ball.color;
        ctx.beginPath();
        ctx.arc(ball.x, ball.y, ball.r, 0, Math.PI * 2);
        // render
        ctx.fill();
    }

    gameLoop(frame, lPad, rPad, ball) {
        console.log("game loop", window.location.href.includes("pong"))
        if (newGame || !window.location.href.includes("pong")) {
            console.log("new gamee")
            return
        }
        if (updatePaddelAndBall) {
            updatePaddelAndBall = false
            rPad = new Paddle("right", this.rightColor);
            lPad = new Paddle("left", this.leftColor);
            ball = new Ball(this.ballColor);
        }
        if (this.beforeGame)
            this.beforeGameLoop()
        else {
            this.draw(lPad, rPad, ball, frame)
            if (this.lPoint > 2 || this.rPoint > 2) {
                ctx.clearRect(0, 0, canvas.width, canvas.height);
                ctx.fillStyle = 'black';
                ctx.fillRect(0, 0, canvas.width, canvas.height);
                ctx.fillStyle = 'white';
                ctx.font = `${124/sizeMultiplier}px Arial`;
                ctx.textAlign = 'center';
                ctx.textBaseline = 'middle'
                if (this.lPoint > 2) {
                    ctx.fillStyle = lPad.color;
                    ctx.fillText("Left win", canvas.width/2, canvas.height/2);
                    // if (!(frame%20)) {
                    //         ball.genParticle( canvas.width/2, -5, "top", lPad.color)
                    //         ball.genParticle( canvas.width, canvas.height/2, "right", lPad.color)
                    //         ball.genParticle( canvas.width/2, canvas.height, "bottom", lPad.color)
                    //         ball.genParticle( 0, canvas.height/2, "left", lPad.color)
                    //     }
                }
                else if (this.rPoint > 2){
                    ctx.fillStyle = rPad.color;
                    ctx.fillText("Right win", canvas.width/2, canvas.height/2);
                    // if (!(frame%20)) {
                    //     ball.genParticle( canvas.width/2, -19, "top", rPad.color)
                    //     ball.genParticle( canvas.width, canvas.height/2+19, "right", rPad.color)
                    //     ball.genParticle( canvas.width/2+19, canvas.height, "bottom", rPad.color)
                    //     ball.genParticle( 0-19, canvas.height/2, "left", rPad.color)
                    // }
                }
                    ball.animateParticles(ctx)
                    ctx.fillStyle = 'gray';
                    ctx.font = `${80/sizeMultiplier}px Arial`;
                    ctx.fillText(`${this.lPoint}:${this.rPoint}`, canvas.width/2, canvas.height/3*2);
                    ctx.fillStyle = 'black'
                    socket.close();
                    sendData = false
                    return 
            }
            else if (this.startGame && socketJsonGame) {
                ball.x = socketJsonGame.ball.x/sizeMultiplier
                ball.y = socketJsonGame.ball.y/sizeMultiplier
                lPad.x = socketJsonGame.lPad.x/sizeMultiplier
                lPad.y = socketJsonGame.lPad.y/sizeMultiplier
                rPad.x = socketJsonGame.rPad.x/sizeMultiplier
                rPad.y = socketJsonGame.rPad.y/sizeMultiplier
                if (socketJsonParticle && socketJsonParticle.color == "rPad") {
                    ball.genParticle(parseInt(socketJsonParticle.x/sizeMultiplier), parseInt(socketJsonParticle.y/sizeMultiplier), socketJsonParticle.side, this.rightColor)
                    socketJsonParticle = ""
                }
                else if (socketJsonParticle && socketJsonParticle.color == "ball") {
                    ball.genParticle(parseInt(socketJsonParticle.x/sizeMultiplier), parseInt(socketJsonParticle.y/sizeMultiplier), socketJsonParticle.side, this.ballColor)
                    socketJsonParticle = ""
                }
                else if (socketJsonParticle && socketJsonParticle.color == "lPad") {
                    ball.genParticle(parseInt(socketJsonParticle.x/sizeMultiplier), parseInt(socketJsonParticle.y/sizeMultiplier), socketJsonParticle.side, this.leftColor)
                    socketJsonParticle = ""
                }
                if (socketJsonPoint) {
                    this.lPoint = socketJsonPoint.left
                    this.rPoint = socketJsonPoint.right
                    socketJsonPoint = ""
                }
            }
            ctx.fillStyle = 'white';
            ctx.font = `${80/sizeMultiplier}px Arial`;
            ctx.textAlign = 'center';
            ctx.textBaseline = 'middle'
            if (socketJsonStartTimming == "[START_GAME]") {
                socketJsonStartTimming = ""
                this.startGame = true
            }
            ctx.fillText(socketJsonStartTimming, canvas.width/2, canvas.height/2-canvas.height/7);
            ctx.font = `${40/sizeMultiplier}px Arial`;
            if (this.playerNb == 1 && !this.startGame) {
                ctx.fillStyle = this.leftColor;
                ctx.fillText("Left player !", canvas.width/2, canvas.height/2+canvas.height/7);
            }
            else if (this.playerNb == 2 && !this.startGame){
                ctx.fillStyle = this.rightColor;
                ctx.fillText("Right player !", canvas.width/2, canvas.height/2+canvas.height/7);
            }
            if (this.stopGame)
                return
        }
        requestAnimationFrame(() => {
            this.gameLoop(++frame, lPad, rPad, ball)
        });
    }
}

class Paddle {
    constructor(side, color) {
        this.init(side, color)
    }
    init(side, color) {
        if (side == "right")
            this.x = canvas.width/100*98
        else
            this.x = canvas.width/100
        this.w = canvas.width/100;
        this.h = canvas.height/5;
        this.y = (canvas.height/2)-(this.h/2)
        this.s = 10
        this.color = color

    }
    up() {
        if (0 < this.y)
            this.y -= this.s;
    }
    down () {
        if (this.y + this.h < canvas.height)
            this.y += this.s;
    }
};

class Particle {
    constructor(startX, startY, side, color) {
        let size = 15
        this.color = color
        this.x = startX;
        this.y = startY;
        this.a = Math.random() + 1
        this.r = 1
        this.s = 1
        let randDir = Math.random()
        let randSide = Math.random()
        let randAlpha = Math.random()
        let randRotate = Math.random()
        let randSize = Math.random()
		// FlipCoin
        if (randSide < 0.5)
            randSide = -1;
        else
            randSide = 1;
        switch (side) {
            case "top":
                this.vecX = ((randDir * this.s) * randSide);
                this.vecY = (1-randDir * this.s);
                break ;
            case "right":
                this.vecX = (randDir * this.s) * -1 ;
                this.vecY = (1-randDir * this.s) * randSide;
                break;
            case "bottom":
                this.vecX = ((randDir * this.s) * randSide);
                this.vecY = (1-randDir * this.s) * -1;
                break;
            case "left":
                this.vecX = ((randDir * this.s) * 1);
                this.vecY = (1-randDir * this.s) *randSide;
                break;
        }
        this.size = size + (size*randSize)
        this.vecSize = randSize
        this.vecA = randAlpha;
        this.vecR = randRotate/20 * randSide;
    }

    draw(ctx) {
        if (this.a - this.vecA < 0 || this.size < 0)
            return "out"
        ctx.fillStyle = this.color;
        ctx.globalAlpha =  this.a - this.vecA;
        ctx.translate(this.x, this.y);
        this.r -= this.vecR
        ctx.rotate(this.r);
        this.size -= this.vecSize
        ctx.fillRect(-10 / 2, -10 / 2, this.size, this.size);
        ctx.setTransform(1, 0, 0, 1, 0, 0);
        ctx.globalAlpha = 1
        return ""
    }

    update() {
        this.x += this.vecX;
        this.y += this.vecY;
    }
}

class Ball {
	constructor(color) {
		this.color = color
		this.init("")
	}

	init(side) {
        let randDir = Math.random().toFixed(2);
        let randSide = Math.random().toFixed(2);

        this.x = canvas.width / 2;
        this.y = canvas.height / 2;
        this.r = 10/sizeMultiplier
        this.nbParticle = 30
        this.particles = []

        if (randSide < 0.5)
            this.vecX = 1
        else
            this.vecX = -1
        if (side === "right")
            this.vecX = 1
        if (side === "left")
            this.vecX = -1
        if (randDir < 0.5)
            this.vecY = (randDir-1)
        else
            this.vecY = randDir
    }

    genParticle(startX, startY, side, color) {
        for (let i = 0; i < this.nbParticle; i++) {
            this.particles.push(new Particle(startX, startY, side, color));
        }
    }

    animateParticles(ctx) {
        for (let particle of this.particles) {
            if(particle.draw(ctx) == "out") {
                    this.particles.splice(this.particles.indexOf(particle), 1);
            }
            particle.update();
        }
    }
};

function sendKeys(data){
    if (sendData)
        socket.send(data)
}

function sendLocalGame(event, value) {
    if (event.key === "w") sendKeys(JSON.stringify({player: "1", key: "up", value: value}));
    if (event.key === "s") sendKeys(JSON.stringify({player: "1", key: "down", value: value}));
    if (event.key === "ArrowUp") sendKeys(JSON.stringify({player: "2", key: "up", value: value}));
    if (event.key === "ArrowDown") sendKeys(JSON.stringify({player: "2", key: "down", value: value}));
}

function initKey() {
    document.addEventListener('keydown', function(event) {
        if (pong.playerNb == -1)
            sendLocalGame(event, true)
        else {

            if (event.key === "w") sendKeys(JSON.stringify({player: pong.playerNb, key: "up", value: true}));
            if (event.key === "s") sendKeys(JSON.stringify({player: pong.playerNb, key: "down", value: true}));
        }
    });
    document.addEventListener('keyup', function(event) {
        if (pong.playerNb == -1)
            sendLocalGame(event, false)
        else {

            if (event.key === "w") sendKeys(JSON.stringify({player: pong.playerNb, key: "up", value: false}));
            if (event.key === "s") sendKeys(JSON.stringify({player: pong.playerNb, key: "down", value: false}));
        }
    });


    socket.onmessage = function(event) {
        dataJson = JSON.parse(event.data)
        if (!("game" in dataJson))
            console.log(dataJson)
        if ("game" in dataJson)
        	socketJsonGame = dataJson.game;
        else if ("startGameIn" in dataJson)
            socketJsonStartTimming = dataJson.startGameIn
        else if ("particle" in dataJson)
            socketJsonParticle = dataJson.particle
        else if ("point" in dataJson)
        	socketJsonPoint = dataJson.point
        else if ("PlayerNumber" in dataJson)
        	pong.playerNb = dataJson.PlayerNumber
        else if ("CancelMatch" in dataJson) {
            console.log("CancelMatch")
            pong.stopGame = true;
            sendData = false
            startSocket(true)
        }
        else if ("errorMessage" in dataJson) {
            pong.beforeGameMsg.splice(pong.beforeGameMsg.indexOf(`waiting for player's side`))
            pong.beforeGameMsg.push(dataJson.errorMessage)
            if (dataJson.errorMessage == "redirect")
                document.location.href = `${window.location.origin}/tournament`
        }
        else if ("check" in dataJson) {
            console.log(dataJson)
            if (dataJson.check == "connectionSetUp")
                socket.send(JSON.stringify({"check":"connectionSetUpOK"}));
        }
        else
			console.log(dataJson)
    };
}

function getIdMatch() {
    var url = new URL(window.location.href);
    console.log("Constructed URL:", url.toString());

    var params = new URLSearchParams(url.search);

    console.log("URLSearchParams:", params.toString());

    var id = params.get("id");
    console.log(`id = ${id}`);
    return id
}

async function startSocket(reMatch) {
    pongCanvasDiv.style.display = "block"
    pongChoise.style.display = "none"
	sizeMultiplier = calculateInvertedMultiplier();
    socketJsonGame = null;
    socketJsonPoint = ""
    socketJsonParticle = "";
    socketJsonStartTimming = "Waiting player ...";
    sendData = true
    ctx.fillStyle = '#0f0f0f';
    ctx.fillRect(0, 0, canvas.width, canvas.height);
    newGame = true
    await new Promise(resolve => setTimeout(resolve, 1000));
    newGame = false
    pong = new Pong("#ff0000", "#00ff00", "#fff", 10, 8)
    socketJsonGame = null;
    socketJsonParticle = "";
    socketJsonStartTimming = "Waiting player ...";
    console.log(reMatch)
    if (reMatch) {
        pong.beforeGameMsg.push(`The opponent is disconnected, search for a new game in 2s `)
        await new Promise(resolve => setTimeout(resolve, 2000));
    }
    socket = new WebSocket(`wss://${window.location.host}/pongSocket/${getIdMatch()}`);
    console.log("HEY THIS IS PONG SOCKET \\/");
    console.log(socket)
    socket.onerror = function(error) {
        console.log(error)
        pong.beforeGameMsg.push(`Connection Error`)
        return
    };
    socket.onclose = function(event) {
        console.log(event)
        pong.beforeGameMsg.push(`Connection Close`)
        return
    };
    pong.beforeGameMsg.push(`Waiting for connection...`)
    socket.onopen = async function(event) {
        pong.beforeGameMsg.push(`Connection OK`)
        console.log('Connection OK');
        pong.beforeGameMsg.push(`waiting for player's side`)
        socket.send(JSON.stringify({"getSidePlayer" : ""}));
        sendData = true
        initKey()
        while (pong.playerNb == 0)
            await new Promise(resolve => setTimeout(resolve, 10));
        console.log(`pong.playerNb = ${pong.playerNb}`)
        pong.beforeGame = false
    };
}
function stopSocket() {
    console.log("close socket")
    if (socket) {
        socket.close()
        newGame = true
    }

}

const pongOnline = document.getElementById("pongOnline")
const pongLocal = document.getElementById("pongLocal")
const pongCanvasDiv = document.getElementById("pongCanvasDiv")
const pongChoise = document.getElementById("pongChoise")
pongOnline.addEventListener("click", e => {
    e.preventDefault()
    pongCanvasDiv.style.display = "block"
    pongChoise.style.display = "none"
    startSocket(false)
})


pongLocal.addEventListener("click", e => {
    e.preventDefault()
    pongCanvasDiv.style.display = "block"
    pongChoise.style.display = "none"
    fetch('/api/getMatchLocal/', {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        window.history.replaceState(null, 'title', '/' + `pong?id=${data.uid}`);
        startSocket(false)
    })
    
})

function startPong(reMatch) {
    console.log("coucou")
}