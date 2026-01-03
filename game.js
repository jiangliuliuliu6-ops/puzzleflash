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
    ctx.beginPath();
    ctx.arc(player.x, player.y, player.radius, 0, Math.PI * 2);
    ctx.fillStyle = player.color;
    ctx.fill();
    ctx.closePath();
}

// 绘制鱼群
function drawFish() {
    fishArray.forEach(fish => {
        ctx.beginPath();
        ctx.arc(fish.x, fish.y, fish.radius, 0, Math.PI * 2);
        ctx.fillStyle = fish.color;
        ctx.fill();
        ctx.closePath();
    });
}

// 更新玩家鱼的位置
function updatePlayer() {
    player.x += player.dx;
    player.y += player.dy;

    // 控制玩家不出界
    if (player.x < 0) player.x = 0;
    if (player.y < 0) player.y = 0;
    if (player.x > canvas.width) player.x = canvas.width;
    if (player.y > canvas.height) player.y = canvas.height;
}

// 移动玩家鱼
function movePlayer(event) {
    if (event.key === "ArrowUp") player.dy = -player.speed;
    if (event.key === "ArrowDown") player.dy = player.speed;
    if (event.key === "ArrowLeft") player.dx = -player.speed;
    if (event.key === "ArrowRight") player.dx = player.speed;
}

// 检查玩家与鱼的碰撞
function checkCollision() {
    fishArray.forEach((fish, index) => {
        const dist = Math.hypot(player.x - fish.x, player.y - fish.y);
        if (dist < player.radius + fish.radius) {
            if (player.radius > fish.radius) {
                // 玩家吃掉鱼
                player.radius += 1;
                fishArray.splice(index, 1); // 移除被吃掉的鱼
            } else {
                // 玩家被鱼吃掉，游戏结束
                alert("Game Over!");
                resetGame();
            }
        }
    });
}

// 游戏重置
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

    // 更新并绘制游戏元素
    updatePlayer();
    drawPlayer();
    drawFish();
    checkCollision();

    requestAnimationFrame(gameLoop);
}

// 按键控制
window.addEventListener("keydown", movePlayer);

// 开始游戏循环
gameLoop();
