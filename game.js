let startTime;
let timeout;

const message = document.getElementById("message");
const result = document.getElementById("result");
const startBtn = document.getElementById("startBtn");
const themeSelector = document.getElementById("themeSelector");

startBtn.addEventListener("click", startGame);

function startGame(){
    result.textContent = "";
    message.textContent = "Wait for green...";
    startBtn.disabled = true;

    const delay = Math.random()*3000 + 1000;

    timeout = setTimeout(()=>{
        document.body.style.background = "#4CAF50";
        message.textContent = "CLICK NOW!";
        startTime = Date.now();

        document.body.addEventListener("click", finishGame);
    }, delay);
}

function finishGame(){
    const reaction = Date.now() - startTime;
    result.textContent = "Your reaction time: " + reaction + " ms";
    resetGame();
}

function resetGame(){
    document.body.style.background = "#f5f5f5";
    startBtn.disabled = false;
    document.body.removeEventListener("click", finishGame);
}

themeSelector.addEventListener("change", ()=>{
    switch(themeSelector.value){
        case "christmas":
            document.body.style.background="#d00000";
            break;
        case "halloween":
            document.body.style.background="#ff9100";
            break;
        case "thanksgiving":
            document.body.style.background="#b5651d";
            break;
        case "independence":
            document.body.style.background="#0033a0";
            break;
        default:
            document.body.style.background="#f5f5f5";
    }
});
