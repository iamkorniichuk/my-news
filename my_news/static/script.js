// TODO: Make a config URL
const URL = "http://127.0.0.1:5000/"

function onNewsClick(id){
    window.location.href = URL + "news/" + id;
}

function onUserClick(login){
    window.location.href = URL + "user/" + login;
}