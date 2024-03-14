const canvas = document.getElementById('pongCanvas');
const ctx = canvas.getContext('2d');






class Pong {
    constructor(rightColor, leftColor, ballColor, speedPadle, speedBall) {
        var rPad = new Paddle("right", rightColor);
        var lPad = new Paddle("left", leftColor);
        var ball = new Ball(ballColor);
        this.playerNb = 0
        this.startGame = false;
        rPad.s = speedPadle
        lPad.s = speedPadle
        ball.s = speedBall

        this.gameLoop(0, rPad, lPad, ball);
    }
    draw(lPad, rPad, ball) {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        
        ctx.fillStyle = 'black';
        ctx.fillRect(0, 0, canvas.width, canvas.height);
        
    
        ctx.fillStyle = lPad.color; 
        ctx.font = '124px Arial';
        ctx.textAlign = 'center';
        ctx.textBaseline = 'middle'
        ctx.fillText(lPad.point, canvas.width/2/2, 100); 
        ctx.fillStyle = rPad.color; 
        ctx.fillText(rPad.point, canvas.width/2 + (canvas.width/2/2), 100); 
    
    
        
        ctx.fillStyle = lPad.color;
        ctx.fillRect(lPad.x, lPad.y, lPad.w, lPad.h);
        ctx.fillStyle = rPad.color;
        ctx.fillRect(rPad.x, rPad.y, rPad.w, rPad.h);
        ball.animateParticles(ctx)
        
        ctx.fillStyle = ball.color;
        ctx.beginPath(); 
        ctx.arc(ball.x, ball.y, ball.r, 0, Math.PI * 2); 
        ctx.fill(); 
    }
    
    
    
    
    gameLoop(frame, lPad, rPad, ball) {
        this.draw(lPad, rPad, ball)
        if (this.startGame) {
            console.log(socketJsonGame)
            ball.x = socketJsonGame.ball.x
            ball.y = socketJsonGame.ball.y
            lPad.x = socketJsonGame.lPad.x
            lPad.y = socketJsonGame.lPad.y
            rPad.x = socketJsonGame.rPad.x
            rPad.y = socketJsonGame.rPad.y
            // if (KeyW)
            //     lPad.up()
            // if (KeyS)
            //     lPad.down()
            // if (ArrowUp)
            //     rPad.up()
            // if (ArrowDown)
            //     rPad.down()
            if (rPad.point > 2 || lPad.point > 2) {
                ctx.clearRect(0, 0, canvas.width, canvas.height);
                ctx.fillStyle = 'black';
                ctx.fillRect(0, 0, canvas.width, canvas.height);
                ctx.fillStyle = 'white'; 
                ctx.font = '124px Arial';
                ctx.textAlign = 'center'; 
                ctx.textBaseline = 'middle'
                if (lPad.point > 2)
                    ctx.fillText("Left win", canvas.width/2, canvas.height/2); 
                else
                    ctx.fillText("Right win", canvas.width/2, canvas.height/2); 
                ctx.fillStyle = 'gray'; 
                ctx.font = '80px Arial';
                ctx.fillText(`${lPad.point}:${rPad.point}`, canvas.width/2, canvas.height/3*2); 
                }
            else 
                ball.moove(lPad, rPad)
            ctx.fillStyle = 'black'
        }
        else {
            ctx.fillStyle = 'white'; 
            ctx.font = '80px Arial';
            ctx.textAlign = 'center'; 
            ctx.textBaseline = 'middle'
            ctx.fillText(socketJsonStartTimming, canvas.width/2, canvas.height/2-canvas.height/7); 
            if (socketJsonStartTimming == "")
                this.startGame = true
                
        }
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
        this.point = 0
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

        // if (randAlpha > 0.5)
        // randAlpha -= 0.5
        // if (randAlpha < 0.2)
        // randAlpha += 0.2
        this.size = size + (size*randSize)
        this.vecSize = randSize
        this.vecA = randAlpha;
        this.vecR = randRotate/20 * randSide;
    }

    draw(ctx) {
        if (this.a - this.vecA < 0 || this.size < 0)
            return "out"
        ctx.fillStyle = this.color;
        if (pong.startGame)
            ctx.globalAlpha =  this.a - this.vecA;
        else
            ctx.globalAlpha = this.a;
        ctx.translate(this.x, this.y);
        if (pong.startGame)
            this.r -= this.vecR
        ctx.rotate(this.r);
        if (pong.startGame)
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
        this.x = canvas.width / 2;
        this.y = canvas.height / 2;
        this.r = 10
        this.nbParticle = 30
        this.particles = []
        let randDir = Math.random().toFixed(2);
        let randSide = Math.random().toFixed(2);
        if (randSide < 0.5)
            this.vecX = 1
        else
            this.vecX = -1
        if (side === "right")
            this.vecX = 1
        if (side === "left")
            this.vecX = -1
        if (randDir < 0.5) {
            this.vecY = (randDir-1)
        }
        else {
            // console.log(randDir)
            this.vecY = randDir
        }
    }
    constructor(color) {
        this.color = color
        this.init("")
    }

   
    moove(lPad, rPad) {
        if (this.x + this.r >= rPad.x && this.y < rPad.y + rPad.h && this.y > rPad.y) {
            this.genParticle(this.x, this.y, "right", rPad.color)

            this.vecX *= -1
        }
        if (this.x - this.r <= lPad.x+lPad.w && this.y < lPad.y + lPad.h && this.y > lPad.y) {
            this.genParticle(this.x, this.y, "left", lPad.color)
            this.vecX *= -1
        }
        if (this.y + this.r > canvas.height) {
            this.genParticle(this.x, this.y, "bottom", this.color)
            this.vecY *= -1
        }
        if (this.y - this.r < 0 ) {
            this.genParticle(this.x, this.y, "top", this.color)
            this.vecY *= -1
        }
        
        if (this.x < 0) {
            this.genParticle(this.x, this.y, "left", this.color)
            rPad.point += 1;
            this.init("right")
            return 
        }
        
        if (this.x > canvas.width){
            lPad.point += 1;
            this.genParticle(this.x, this.y, "right", this.color)
            this.init("left")
            return ;
        }
        this.x += parseFloat(this.vecX * this.s);
        this.y += parseFloat(this.vecY * this.s);
    }
    genParticle (startX, startY, side, color) {
        for (let i = 0; i < this.nbParticle; i++) {
            this.particles.push(new Particle(startX, startY, side, color));
        }
    }
    animateParticles(ctx) {
        for (let particle of this.particles) {
            particle.draw(ctx);
            if (pong.startGame) {
                particle.update();
            }
        }
    }

};



var ArrowUp = false
var ArrowDown = false
var KeyW = false
var KeyS = false

var pong = new Pong("#ff5000", "#5f50f0", "#fff", 10, 8)

function initKey(socket) {
    document.addEventListener('keydown', function(event) {
        var keyCode = event.key;
        if (keyCode === "w" && !ArrowUp) {
            socket.send(JSON.stringify({player: pong.playerNb, key: "up", value: true}));
            ArrowUp = true
        }
        else if (keyCode === "s" && !ArrowDown) {
            socket.send(JSON.stringify({player: pong.playerNb, key: "down", value: true}));
            ArrowDown = true
        }
        else if(keyCode === "g" && pong.startGame)
            pong.startGame = false
        else if(keyCode === "g" && !pong.startGame)
            pong.startGame = true
    });
    document.addEventListener('keyup', function(event) {
        var keyCode = event.key;
        if (keyCode === "w") {
            socket.send(JSON.stringify({player: pong.playerNb, key: "up", value: false}));
            ArrowUp = false
        }
        else if (keyCode === "s") {
            socket.send(JSON.stringify({player: pong.playerNb, key: "down", value: false}));
            ArrowDown = false
        }
    });
}



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

var token = getCookie('PongToken');
var socketJsonGame;
var socketJsonStartTimming = "Waiting player ...";
var socket;

async function startSocket(matchData) {
    console.log(matchData, matchData.player)
    pong.playerNb = matchData.player
    socket = new WebSocket(`ws://localhost:8000/match`);
    while (!(socket.readyState === WebSocket.OPEN)) {
        console.log('En attente de connexion...');
        await new Promise(resolve => setTimeout(resolve, 1000));
    }
    socket.send(JSON.stringify({"Bonjour,":" serveur!"}));
    console.log("Socket ok")
    initKey(socket)
    socket.onmessage = function(event) {
        dataJson = JSON.parse(event.data)
        if ("game" in dataJson)
            socketJsonGame = dataJson.game;
        else if ("startGameIn" in dataJson) {
            socketJsonStartTimming = dataJson.startGameIn
        }
        else
            console.log(dataJson)
    }; 
}


if (token) {    
    fetch("http://127.0.0.1:8000/api/pong/getIdMatch")
    .then(response => {
        if (!response.ok) {throw new Error('La requête a échoué');}return response.json(); })
    .then(data => {
        if ("error" in data) {
            console.log(data)
            return;
        }
        else {
            startSocket(data.ok);
        }
    })       
}