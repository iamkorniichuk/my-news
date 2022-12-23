// TODO: Make a config URL
const URL = "http://127.0.0.1:5000"

function onNewsClick(id){
    window.location.href = URL + "/news/" + id;
}

function onUserClick(login){
    window.location.href = URL + "/user/" + login;
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

function onLogoutClick(){
    localStorage.clear()
}