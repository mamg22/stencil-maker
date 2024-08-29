const create_button = document.getElementById("create-button");

function create_shortcut_handler(event) {
    if (event.ctrlKey && event.key == 'Enter') {
        create_button.click()
    }
}

window.addEventListener('keyup', create_shortcut_handler)
