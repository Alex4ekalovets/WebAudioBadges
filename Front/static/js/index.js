let audioElements = document.getElementsByTagName('audio');

for (let i = 0; i < audioElements.length; i++) {
    audioElements[i].addEventListener("playing", function () {
        playNewAudio(this);
    });
}

function playNewAudio(newAudio) {
    for (let i = 0; i < audioElements.length; i++) {
        if (audioElements[i] !== newAudio) {
            audioElements[i].pause();
            audioElements[i].currentTime = 0;
        }
    }
    newAudio.play();
}
