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

function onLogoutClick(){
    localStorage.clear()
}