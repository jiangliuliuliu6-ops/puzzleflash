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
    image: new Image(),
};

// 加载玩家鱼的图片
player.image.src = 'playerFish.png';  // 使用一张鱼的图片替换圆点

// 鱼群数据
let fishArray = [];
for (let i = 0; i < 10; i++) {
    let fish = {
        x: Math.random() * canvas.width,
        y: Math.random() * canvas.height,
        radius: Math.random() * 10 + 10,
        image: new Image(),
        dx: Math.random() * 2 - 1,
        dy: Math.random() * 2 - 1,
    };
    fish.image.src = `fish${Math.floor(Math.random() * 10) + 1}.png`;  // 随机选择不同鱼的图片
    fishArray.push(fish);
}

// 绘制玩家鱼
function drawPlayer() {
    ctx.drawImage(player.image, player.x - player.radius, player.y - player.radius, player.radius * 2, player.radius * 2);
}

// 绘制鱼群
function drawFish() {
    fishArray.forEach(fish => {
        ctx.drawImage(fish.image, fish.x - fish.radius, fish.y - fish.radius, fish.radius * 2, fish.radius * 2);
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

// 游戏重置
function resetGame() {
    player.x = canvas.width / 2;
    player.y = canvas.height / 2;
    player.radius = 20;
    fishArray = [];
    for (let i = 0; i < 10; i++) {
        let fish = {
            x: Math.random() * canvas.width,
            y: Math.random() * canvas.height,
            radius: Math.random() * 10 + 10,
            image: new Image(),
            dx: Math.random() * 2 - 1,
            dy: Math.random() * 2 - 1,
        };
        fish.image.src = `fish${Math.floor(Math.random() * 10) + 1}.png`;  // 随机选择不同鱼的图片
        fishArray.push(fish);
    }
}

// 游戏主循环
let gameInterval;
function gameLoop() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    updatePlayer();
    drawPlayer();
    drawFish();
    checkCollision();
}

// 游戏控制
let isGameRunning = false;

// 开始/暂停按钮功能
function toggleGame() {
    if (isGameRunning) {
        clearInterval(gameInterval);
        isGameRunning = false;
    } else {
        gameInterval = setInterval(gameLoop, 1000 / 60); // 每秒60帧
        isGameRunning = true;
    }
}

// 按键控制
window.addEventListener("keydown", movePlayer);

// 控制游戏开关
document.getElementById("startPauseBtn").addEventListener("click", toggleGame);

// 页面初始化时调用
resetGame();
