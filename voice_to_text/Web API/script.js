const startBtn = document.getElementById("startBtn");
const stopBtn = document.getElementById("stopBtn");
const output = document.getElementById("output");

let recognition;

if ("webkitSpeechRecognition" in window || "SpeechRecognition" in window) {
  const SpeechRecognition =
    window.SpeechRecognition || window.webkitSpeechRecognition;
  recognition = new SpeechRecognition();
  recognition.continuous = true;
  recognition.lang = "en-US";

  recognition.onresult = function (event) {
    const transcript = Array.from(event.results)
      .map((result) => result[0].transcript)
      .join("");
    output.value = transcript;
  };

  recognition.onerror = function (event) {
    console.error("Speech recognition error:", event.error);
  };

  startBtn.addEventListener("click", () => {
    recognition.start();
    startBtn.disabled = true;
    stopBtn.disabled = false;
  });

  stopBtn.addEventListener("click", () => {
    recognition.stop();
    startBtn.disabled = false;
    stopBtn.disabled = true;
  });
} else {
  alert("Sorry, your browser does not support Speech Recognition.");
  startBtn.disabled = true;
}
