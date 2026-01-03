let gameButton = document.getElementById("gameButton");
let message = document.getElementById("message");
let result = document.getElementById("result");
let highscores = document.getElementById("highscores");
let themeSelect = document.getElementById("theme");
let difficulty = document.getElementById("difficulty");

let startTime;
let waiting = false;
let ready = false;

function getDelay() {
  if (difficulty.value === "easy") return Math.random() * 2000 + 1000;
  if (difficulty.value === "medium") return Math.random() * 2000 + 500;
  return Math.random() * 1500 + 300;
}

gameButton.addEventListener("click", () => {
  if (!waiting && !ready) {
    message.textContent = "Get ready...";
    gameButton.textContent = "Wait...";
    waiting = true;

    setTimeout(() => {
      ready = true;
      waiting = false;
      gameButton.classList.add("ready");
      gameButton.textContent = "CLICK NOW!";
      startTime = Date.now();
    }, getDelay());
  } 
  else if (waiting) {
    result.textContent = "Too early! ❌";
  }
  else if (ready) {
    let time = Date.now() - startTime;
    result.textContent = `Your time: ${time} ms ⚡`;
    saveScore(time);

    ready = false;
    gameButton.classList.remove("ready");
    gameButton.textContent = "Play Again";
  }
});

function saveScore(score) {
  let data = JSON.parse(localStorage.getItem("scores") || "[]");
  data.push(score);
  data.sort((a,b)=>a-b);
  data = data.slice(0,5);
  localStorage.setItem("scores", JSON.stringify(data));
  renderScores();
}

function renderScores() {
  let data = JSON.parse(localStorage.getItem("scores") || "[]");
  highscores.innerHTML = "";
  data.forEach(s=>{
    let li=document.createElement("li");
    li.textContent = s + " ms";
    highscores.appendChild(li);
  });
}
renderScores();

themeSelect.addEventListener("change", ()=>{
  document.body.className = themeSelect.value;
});
