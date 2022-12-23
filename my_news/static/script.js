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
        data: {'show': true},
        type: 'post',
        success: function(data){ 
            $('.modal-body').html(data);
            $('.modal-body').append(data.htmlresponse);
            $('#empModal').modal('show'); 
        }
    });
}

function onLogoutClick(){
    localStorage.clear()
}