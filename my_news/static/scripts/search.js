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