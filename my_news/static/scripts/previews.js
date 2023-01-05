function previewImages(field){
    if (field.files && field.files[0]) 
    {
        let div = field.nextElementSibling
        div.innerHTML = ''
        for(const image of field.files){

            var reader = new FileReader();

            reader.onload = function (e) {
                let wrap = document.createElement('div')
                wrap.classList.add('col-4')

                let img = document.createElement('img')
                img.src = e.target.result
                img.classList.add('w-100')
                img.classList.add('m-1')

                wrap.appendChild(img)
                div.appendChild(wrap)
            }

            reader.readAsDataURL(image)
        }
    }
}

function deletePreviews(element){
    if(element.tagName.toLowerCase() != 'form'){
        element = element.closest('form')
    }
    let previews = element.querySelectorAll('.preview')
    for(const preview of previews){
        preview.innerHTML = ''
    }
}