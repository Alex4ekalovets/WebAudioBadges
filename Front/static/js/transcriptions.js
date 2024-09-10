let editTextAreas = document.querySelectorAll(".edit-area")

for (let i = 0; i < editTextAreas.length; i++) {
    editTextAreas[i].addEventListener("change", saveTextToFile);
}

async function saveTextToFile(e) {
    let file_data = {
        text: e.target.value,
        record_number: e.target.id
    }
    const response = await fetch(
        "http://172.20.3.134:5002/save_text", {
            method: "POST",
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(file_data)
        })
    if (response.ok) {
        console.log(`Текст записи ${e.target.id} успешно сохранен!`)
    } else {
        console.log(`Не удалось сохранить изменения в тексте записи ${e.target.id}`)
    }
}


async function getDictionary() {
    try {
        const response = await fetch('/patterns');
        const data = await response.json();
        highlightAll(data);
    } catch (error) {
        console.error('Error:', error);
    }
}


function highlightText(inputText, pattern, color, name) {
    const regex = new RegExp(pattern, 'gi');
    const highlightedText = inputText.replace(regex, (match) => {
        return `<span class="badge badge-${color}" data-toggle="tooltip" data-placement="top" title="${name}">${match}</span>`;
    });

    return highlightedText;
}

function highlightAll(dictionary) {
    const transcriptionElements = document.querySelectorAll('.transcription');

    transcriptionElements.forEach(element => {
        let text = element.textContent || element.innerText;
        for (let item in dictionary['Pattern']) {
            text = highlightText(text, dictionary['Pattern'][item], dictionary['Color'][item], item);
        }
        element.innerHTML = text
    });
}


$(document).ready(() => {
    $('[data-toggle="tooltip"]').tooltip()
    getDictionary()

})
