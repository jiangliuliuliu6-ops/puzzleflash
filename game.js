const canvas = document.getElementById("gameCanvas");
const ctx = canvas.getContext("2d");

canvas.width = window.innerWidth;
canvas.height = window.innerHeight;

// 玩家鱼的参数
let player = {
    x: canvas.width / 2,
    y: canvas.height / 2,
    radius: 20,
    speed: 5,
    color: "blue",
    dx: 0,
    dy: 0,
};

// 鱼群数据
let fishArray = [];
for (let i = 0; i < 10; i++) {
    fishArray.push({
        x: Math.random() * canvas.width,
        y: Math.random() * canvas.height,
        radius: Math.random() * 10 + 10,
        color: "green",
        dx: Math.random() * 2 - 1,
        dy: Math.random() * 2 - 1,
    });
}

// 绘制玩家鱼
function drawPlayer() {
    let grad = ctx.createRadialGradient(player.x, player.y, 0, player.x, player.y, player.radius);
    grad.addColorStop(0, "lightblue");
    grad.addColorStop(1, "blue");

    ctx.shadowColor = "rgba(0, 0, 0, 0.5)";
    ctx.shadowBlur = 10;

    ctx.beginPath();
    ctx.arc(player.x, player.y, player.radius, 0, Math.PI * 2);
    ctx.fillStyle = grad;
    ctx.fill();
    ctx.closePath();

    ctx.shadowColor = "transparent";
    ctx.shadowBlur = 0;
}

// 绘制鱼群
function drawFish() {
    fishArray.forEach(fish => {
        let grad = ctx.createRadialGradient(fish.x, fish.y, 0, fish.x, fish.y, fish.radius);
        grad.addColorStop(0, "lightgreen");
        grad.addColorStop(1, "green");

        ctx.shadowColor = "rgba(0, 0, 0, 0.3)";
        ctx.shadowBlur = 5;

        ctx.beginPath();
        ctx.arc(fish.x, fish.y, fish.radius, 0, Math.PI * 2);
        ctx.fillStyle = grad;
        ctx.fill();
        ctx.closePath();

        ctx.shadowColor = "transparent";
        ctx.shadowBlur = 0;
    });
}

// 更新玩家位置
function updatePlayer() {
    player.x += player.dx;
    player.y += player.dy;

    if (player.x < 0) player.x = 0;
    if (player.y < 0) player.y = 0;
    if (player.x > canvas.width) player.x = canvas.width;
    if (player.y > canvas.height) player.y = canvas.height;
}

// 移动玩家
function movePlayer(event) {
    if (event.key === "ArrowUp") player.dy = -player.speed;
    if (event.key === "ArrowDown") player.dy = player.speed;
    if (event.key === "ArrowLeft") player.dx = -player.speed;
    if (event.key === "ArrowRight") player.dx = player.speed;
}

// 检查碰撞
function checkCollision() {
    fishArray.forEach((fish, index) => {
        const dist = Math.hypot(player.x - fish.x, player.y - fish.y);
        if (dist < player.radius + fish.radius) {
            if (player.radius > fish.radius) {
                player.radius += 1;
                fishArray.splice(index, 1);
            } else {
                alert("Game Over!");
                resetGame();
            }
        }
    });
}

// 重置游戏
function resetGame() {
    player.x = canvas.width / 2;
    player.y = canvas.height / 2;
    player.radius = 20;
    fishArray = [];
    for (let i = 0; i < 10; i++) {
        fishArray.push({
            x: Math.random() * canvas.width,
            y: Math.random() * canvas.height,
            radius: Math.random() * 10 + 10,
            color: "green",
            dx: Math.random() * 2 - 1,
            dy: Math.random() * 2 - 1,
        });
    }
}

// 游戏主循环
function gameLoop() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    updatePlayer();
    drawPlayer();
    drawFish();
    checkCollision();
    requestAnimationFrame(gameLoop);
}

// 按键控制
window.addEventListener("keydown", movePlayer);

// 启动游戏循环
gameLoop();
