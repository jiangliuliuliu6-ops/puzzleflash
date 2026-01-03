let startTime;
let timeout;

const message = document.getElementById("message");
const result = document.getElementById("result");
const timeDisplay = document.getElementById("time");
const startBtn = document.getElementById("startBtn");
const themeSelector = document.getElementById("themeSelector");

startBtn.addEventListener("click", startGame);

function startGame(){
    result.style.display = "none"; // Hide result text until the game ends
    timeDisplay.textContent = "";
    message.textContent = "Wait for green...";
    startBtn.disabled = true;

    const delay = Math.random() * 3000 + 1000;

    timeout = setTimeout(()=>{
        document.body.style.backgroundColor = "#4CAF50"; // Green color
        message.textContent = "CLICK NOW!";
        startTime = Date.now();

        document.body.addEventListener("click", finishGame);
    }, delay);
}

function finishGame(){
    const reaction = Date.now() - startTime;
    timeDisplay.textContent = reaction; // Show reaction time
    result.style.display = "block";
    resetGame();
}

function resetGame(){
    document.body.style.backgroundColor = "#f5f5f5"; // Reset background
    startBtn.disabled = false;
    document.body.removeEventListener("click", finishGame);
}

themeSelector.addEventListener("change", ()=>{
    switch(themeSelector.value){
        case "christmas":
            document.body.style.backgroundColor = "#d00000"; // Christmas theme
            break;
        case "halloween":
            document.body.style.backgroundColor = "#ff9100"; // Halloween theme
            break;
        case "thanksgiving":
            document.body.style.backgroundColor = "#b5651d"; // Thanksgiving theme
            break;
        case "independence":
            document.body.style.backgroundColor = "#0033a0"; // Independence Day theme
            break;
        default:
            document.body.style.backgroundColor = "#f5f5f5"; // Default theme
    }
});
