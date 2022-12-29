function onNewsClick(id){
    window.location.href = "/news/" + id;
}

function onUserClick(login){
    window.location.href = "/user/" + login;
}

function onEditClick(url){
    $.ajax({
        url: url,
        type: 'post',
        data: {'show': true},
        success: 
            function(data){
                renderModal(data)
            }
    });
}

function onSubmit(url){
    $.ajax({
        url: url,
        data: new FormData(document.getElementById('modalForm')),
        processData: false,
        contentType: false,
        type: 'post',
        success: 
            function(data){
                if(data.htmlresponse){
                    renderModal(data)
                }else{
                    location.reload()
                }
            }
    });
}

function renderModal(data){
    $('.modal-body').html(data);
    $('.modal-body').append(data.htmlresponse);
    $('#empModal').modal('show');
}

function loadSection(url, id){
    $.ajax({
        url: url,
        type: 'post',
        success: 
            function(data){
                $(`#${id}`).html(data);
                $(`#${id}`).append(data.htmlresponse);
            }
    });
}

function clearHistory(){
    localStorage.clear()
}

function previewImages(field){
    if (field.files && field.files[0]) 
    {
        let div = field.nextElementSibling
        div.innerHTML = ''
        for(const image of field.files){

            var reader = new FileReader();

            reader.onload = function (e) {
                let img = document.createElement('img')
                img.src = e.target.result
                img.classList.add('my-1')
                img.classList.add('w-100')
                div.appendChild(img)
            }

            reader.readAsDataURL(image)
        }
    }
}

function clearForm(button){
    let form = button.closest('form')
    let previews = form.querySelectorAll('.preview')
    for(const preview of previews){
        preview.innerHTML = ''
    }
}