document.getElementById("playSound").addEventListener("click", () => {
  const beep = document.getElementById("beep");
  beep.currentTime = 0;
  beep.play();
});