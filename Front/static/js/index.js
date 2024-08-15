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


let editTextAreas = document.querySelectorAll(".edit-area")

for (let i = 0; i < editTextAreas.length; i++) {
     editTextAreas[i].addEventListener("click", saveTextToFile);
 }

async function saveTextToFile(e) {
    let file_data = {
        text: e.target.value,
        record_number: e.target.id
    }
    const response = await fetch(
        "http://172.20.3.134:5002/save_text", {
            method: "POST",
            body: JSON.stringify(file_data)
        })
    if (response.ok) {
        console.log(`Текст записи ${e.target.id} успешно сохранен!`)
    } else {
        console.log(`Не удалось сохранить изменения в тексте записи ${e.target.id}`)
    }
}