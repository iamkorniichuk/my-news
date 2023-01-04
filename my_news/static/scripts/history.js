function clearHistory(){
    localStorage.clear()
}

function addToHistory(news_id){
    localStorage.setItem('history', addNews(news_id))
}

function addNews(news_id){
    // TODO: no time when opened
    let history = JSON.parse(localStorage.getItem('history'))
    if(history !== null){
        history.push(news_id)
    }else{
        history = [news_id]
    }
    return JSON.stringify(history)
}