localStorage.setItem('history', add_news())

function add_news(){
    // TODO: repeating values + no time when opened
    let history = JSON.parse(localStorage.getItem('history'))
    if(history !== null){
        history.push(get_news_id())
    }else{
        history = [get_news_id()]
    }
    return JSON.stringify(history)
}

function get_news_id(){
    let path = location.pathname
    return path.slice(path.lastIndexOf('/') + 1)
}