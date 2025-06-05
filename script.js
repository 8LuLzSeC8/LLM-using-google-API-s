const recordButton = document.getElementById('record');
const stopButton = document.getElementById('stop');
const audioElement = document.getElementById('audio');
const uploadForm = document.getElementById('uploadForm');
const audioDataInput = document.getElementById('audioData');
const timerDisplay = document.getElementById('timer');

let mediaRecorder;
let audioChunks = [];
let startTime;

function formatTime(time) {
  const minutes = Math.floor(time / 60);
  const seconds = Math.floor(time % 60);
  return `${minutes}:${seconds.toString().padStart(2, '0')}`;
}

recordButton.addEventListener('click', () => {
  navigator.mediaDevices.getUserMedia({ audio: true })
    .then(stream => {
      mediaRecorder = new MediaRecorder(stream);
      mediaRecorder.start();

      startTime = Date.now();
      let timerInterval = setInterval(() => {
        const elapsedTime = Math.floor((Date.now() - startTime) / 1000);
        timerDisplay.textContent = formatTime(elapsedTime);
      }, 1000);

      mediaRecorder.ondataavailable = e => {
        audioChunks.push(e.data);
      };

      mediaRecorder.onstop = () => {
        const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
        const formData = new FormData();
        formData.append('audio_data', audioBlob, 'recorded_audio.wav');

        fetch('/upload', {
            method: 'POST',
            body: formData
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            location.reload(); // Force refresh

            return response.text();
        })
        .then(data => {
            console.log('Audio uploaded successfully:', data);
            // Redirect to playback page or display success message
        })
        .catch(error => {
            console.error('Error uploading audio:', error);
        });
      };
    })
    .catch(error => {
      console.error('Error accessing microphone:', error);
    });

  recordButton.disabled = true;
  stopButton.disabled = false;
});

stopButton.addEventListener('click', () => {
  if (mediaRecorder) {
    mediaRecorder.stop();
  }

  recordButton.disabled = false;
  stopButton.disabled = true;
});

// Initially disable the stop button
stopButton.disabled = true;

function showText(filename) {
    var textDisplay = document.getElementById('textDisplay-' + filename);
    
    // Toggle the display
    if (textDisplay.style.display === "none") {
        // Create a new XMLHttpRequest object to fetch the text content
        var xhr = new XMLHttpRequest();
        xhr.onreadystatechange = function () {
            if (xhr.readyState == 4 && xhr.status == 200) {
                // Set the content of the paragraph to the text file content
                textDisplay.innerText = xhr.responseText;
                textDisplay.style.display = "block";
            }
        };
        // Make the GET request to retrieve the text file
        xhr.open("GET", "uploads/" + filename + ".txt", true);
        xhr.send();

        document.getElementById('Transcript').innerText = "Close Transcript"
    } else {
        // Hide the text if it's already displayed
        textDisplay.style.display = "none";
        document.getElementById('Transcript+{{file}}').innerText = "Transcription"
    }
}

