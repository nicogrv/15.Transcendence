const canvas = document.getElementById('pongCanvas');
const ctx = canvas.getContext('2d');

var token
var socket;
var ArrowUp = false
var ArrowDown = false
var KeyW = false
var KeyS = false
var pong
var socketJsonGame = null;
var socketJsonPoint
var socketJsonParticle = "";
var socketJsonStartTimming = "Waiting player ...";
var sendData = true

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

token = getCookie('PongToken');

class Pong {
    constructor(rightColor, leftColor, ballColor, speedPadle, speedBall) {
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
        this.gameLoop(0, rPad, lPad, ball);
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
    draw(lPad, rPad, ball) {
        // clear screen
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        // color background
        ctx.fillStyle = '#0f0f0f';
        ctx.fillRect(0, 0, canvas.width, canvas.height);
        // display point
        ctx.fillStyle = lPad.color; 
        ctx.font = '124px Arial';
        ctx.textAlign = 'center';
        ctx.textBaseline = 'middle'
        ctx.fillText(this.lPoint, canvas.width/2/2, 100); 
        ctx.fillStyle = rPad.color; 
        ctx.fillText(this.rPoint, canvas.width/2 + (canvas.width/2/2), 100); 
        // fill pad
        ctx.fillStyle = lPad.color;
        ctx.fillRect(lPad.x, lPad.y, lPad.w, lPad.h);
        ctx.fillStyle = rPad.color;
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
        if (this.beforeGame)
            this.beforeGameLoop()
        else {
            this.draw(lPad, rPad, ball)
            if (this.lPoint > 2 || this.rPoint > 2) {
                ctx.clearRect(0, 0, canvas.width, canvas.height);
                ctx.fillStyle = 'black';
                ctx.fillRect(0, 0, canvas.width, canvas.height);
                ctx.fillStyle = 'white'; 
                ctx.font = '124px Arial';
                ctx.textAlign = 'center'; 
                ctx.textBaseline = 'middle'
                if (this.lPoint > 2) {
                    ctx.fillStyle = lPad.color; 
                    if (!(frame%10)) {
                        ball.genParticle( canvas.width/2, 0, "top", lPad.color)
                        ball.genParticle( canvas.width, canvas.height/2, "right", lPad.color)
                        ball.genParticle( canvas.width/2, canvas.height, "bottom", lPad.color)
                        ball.genParticle( 0, canvas.height/2, "left", lPad.color)
                    }
                    ctx.fillText("Left win", canvas.width/2, canvas.height/2); 
                }
                else {
                    if (!(frame%10)) {
                        ball.genParticle( canvas.width/2, 0, "top", rPad.color)
                        ball.genParticle( canvas.width, canvas.height/2, "right", rPad.color)
                        ball.genParticle( canvas.width/2, canvas.height, "bottom", rPad.color)
                        ball.genParticle( 0, canvas.height/2, "left", rPad.color)
                    }
                    // ctx.fillStyle = rPad.color; 
                    ctx.fillText("Right win", canvas.width/2, canvas.height/2); 
                }
                ball.animateParticles(ctx)
                ctx.fillStyle = 'gray'; 
                ctx.font = '80px Arial';
                ctx.fillText(`${this.lPoint}:${this.rPoint}`, canvas.width/2, canvas.height/3*2); 
                ctx.fillStyle = 'black'
                if (this.updateStat) {
                    setTimeout(function() {
                        document.getElementById("topBarName").setAttribute("needupdate", "true")
                    }, 5000)
                    this.updateStat = false
                }
                sendData = false
                socket.close();
            }
            else if (this.startGame && socketJsonGame) {
                ball.x = socketJsonGame.ball.x
                ball.y = socketJsonGame.ball.y
                lPad.x = socketJsonGame.lPad.x
                lPad.y = socketJsonGame.lPad.y
                rPad.x = socketJsonGame.rPad.x      
                rPad.y = socketJsonGame.rPad.y
                if (socketJsonParticle && socketJsonParticle.color == "rPad") {
                    ball.genParticle(parseInt(socketJsonParticle.x), parseInt(socketJsonParticle.y), socketJsonParticle.side, this.rightColor)
                    socketJsonParticle = ""
                }
                else if (socketJsonParticle && socketJsonParticle.color == "ball") {
                    ball.genParticle(parseInt(socketJsonParticle.x), parseInt(socketJsonParticle.y), socketJsonParticle.side, this.ballColor)
                    socketJsonParticle = ""
                }
                else if (socketJsonParticle && socketJsonParticle.color == "lPad") {
                    ball.genParticle(parseInt(socketJsonParticle.x), parseInt(socketJsonParticle.y), socketJsonParticle.side, this.leftColor)
                    socketJsonParticle = ""
                }
                if (socketJsonPoint) {
                    this.lPoint = socketJsonPoint.left
                    this.rPoint = socketJsonPoint.right
                    socketJsonPoint = ""
                }
            }
            ctx.fillStyle = 'white'; 
            ctx.font = '80px Arial';
            ctx.textAlign = 'center'; 
            ctx.textBaseline = 'middle'
            ctx.fillText(socketJsonStartTimming, canvas.width/2, canvas.height/2-canvas.height/7); 
            ctx.font = '40px Arial';
            if (this.playerNb == 1 && !this.startGame) {
                ctx.fillStyle = this.leftColor; 
                ctx.fillText("Right player !", canvas.width/2, canvas.height/2+canvas.height/7); 
            }
            else if (this.playerNb == 2 && !this.startGame){
                ctx.fillStyle = this.rightColor; 
                ctx.fillText("Left player !", canvas.width/2, canvas.height/2+canvas.height/7); 
            }
            if (socketJsonStartTimming == "")
            this.startGame = true 
        }
        if (this.stopGame)
            return 
        requestAnimationFrame(() => {
            this.gameLoop(++frame, lPad, rPad, ball)
        });
    }
}

class Paddle {
    constructor(side, color) {
        if (side == "right")
            this.x = canvas.width/100
        else
            this.x = canvas.width/100*98
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
    init(side) {
        let randDir = Math.random().toFixed(2);
        let randSide = Math.random().toFixed(2);
        
        this.x = canvas.width / 2;
        this.y = canvas.height / 2;
        this.r = 10
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
    constructor(color) {
        this.color = color
        this.init("")
    }


    genParticle(startX, startY, side, color) {
        for (let i = 0; i < this.nbParticle; i++) {
            this.particles.push(new Particle(startX, startY, side, color));
        }
    }
    animateParticles(ctx) {
        for (let particle of this.particles) {
            particle.draw(ctx);
            particle.update();
        }
    }

};

function sendKeys(data){
    if (sendData)
        socket.send(data)
}
function initKey() {
    document.addEventListener('keydown', function(event) {
        var keyCode = event.key;
        if (keyCode === "w" && !ArrowUp) {
            sendKeys(JSON.stringify({player: pong.playerNb, key: "up", value: true}));
            ArrowUp = true
        }
        else if (keyCode === "s" && !ArrowDown) {
            sendKeys(JSON.stringify({player: pong.playerNb, key: "down", value: true}));
            ArrowDown = true
        }
        else if (keyCode === "n") {
            console.log("NEXT")
            sendKeys(JSON.stringify({"nextFrame":"ok"}));
        }
        else if(keyCode === "g" && pong.startGame)
            pong.startGame = false
        else if(keyCode === "g" && !pong.startGame)
            pong.startGame = true
    });
    document.addEventListener('keyup', function(event) {
        var keyCode = event.key;
        if (keyCode === "w") {
            console.log(JSON.stringify({player: pong.playerNb, key: "up", value: false}))
            sendKeys(JSON.stringify({player: pong.playerNb, key: "up", value: false}));
            ArrowUp = false
        }
        else if (keyCode === "s") {
            sendKeys(JSON.stringify({player: pong.playerNb, key: "down", value: false}));
            ArrowDown = false
        }
    });


    socket.onmessage = function(event) {
        dataJson = JSON.parse(event.data)
        dataJson = dataJson.message
        if ("game" in dataJson)
            socketJsonGame = dataJson.game;
        else if ("startGameIn" in dataJson)
            socketJsonStartTimming = dataJson.startGameIn
        else if ("particle" in dataJson) 
            socketJsonParticle = dataJson.particle
        else if ("point" in dataJson)
            socketJsonPoint = dataJson.point
        else if ("PlayerNumber" in dataJson) {
            console.log(dataJson.uid)
            pong.playerNb = dataJson.PlayerNumber
        }
        else if ("CancelMatch" in dataJson) {
            pong.stopGame = true;
            startSocket(true, 2)
        }
        else
            console.log(dataJson)
    }; 
}

async function startSocket(reMatch) {
    pong = new Pong("#ff5000", "#5f50f0", "#fff", 10, 8)
    ArrowUp = false
    ArrowDown = false
    KeyW = false
    KeyS = false
    socketJsonGame = null;
    socketJsonParticle = "";
    socketJsonStartTimming = "Waiting player ...";
    let stopSocketConnection = false
    if (reMatch) {
        pong.beforeGameMsg.push(`The opponent is disconnected, search for a new game in 5s `)
        await new Promise(resolve => setTimeout(resolve, 5000));
       console.log("front")
    }
    console.log("back")
    socket = new WebSocket(`ws://127.0.0.1:8000/match/${token}`);
    pong.beforeGameMsg.push(`New socket`)
    socket.onerror = function(error) {
        stopSocketConnection = true
        pong.beforeGameMsg.push(`Socket Error`)
        return
    };
    socket.onclose = function(event) {
        stopSocketConnection = true
        pong.beforeGameMsg.push(`Socket Close`)
        return 
    };
    pong.beforeGameMsg.push(`Waiting for connection...`)
    while (socket.readyState != WebSocket.OPEN) {
        console.log('Waiting for connection...');
        if (stopSocketConnection)
            return 
        await new Promise(resolve => setTimeout(resolve, 100));
    }
    pong.beforeGameMsg.push(`Connection OK`)
    console.log('Connection OK');
    initKey()
    pong.beforeGameMsg.push(`waiting for player's side`)
    while (pong.playerNb == 0) {
        await new Promise(resolve => setTimeout(resolve, 100));
    }
    pong.beforeGame = false
}
if (token)
    startSocket(false);
