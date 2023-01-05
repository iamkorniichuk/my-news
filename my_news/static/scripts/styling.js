function changeIcon(checkbox, icons){
    let icon = checkbox.nextElementSibling
    if(checkbox.checked){
        icon.classList.add(icons[1]);
        icon.classList.remove(icons[0]);
    }else{
        icon.classList.add(icons[0]);
        icon.classList.remove(icons[1]);
    }
}

function fillStars(element){
    let radio = element.parentElement.parentElement
    let buttons = radio.children
    let allChecked = false
    for (const button of buttons) {
        if(allChecked) button.classList.remove('active')
        else button.classList.add('active')
        if(button === element.parentElement) allChecked = true
    }
}

function renderStars(){
    let ratings = document.getElementsByClassName('star-rating')
    let all_buttons = []
    for (const rating of ratings) {
        all_buttons.push(rating.children)
    }
    for (const buttons of all_buttons) {
        let allChecked = false
        for (const button of buttons) {
            if(allChecked) button.classList.remove('active')
            else button.classList.add('active')
            if(button.getElementsByTagName('input')[0].checked) allChecked = true
        }
    }
}