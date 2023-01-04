class Request{
    constructor(action){
        this.action = action
    }

    set onSuccess(func){
        this.onSuccessStatus = function(){ func() }
    }

    send(){
        let obj = this
        $.ajax({
            async: false,
            url: obj.action,
            type: 'post',
            success: 
                function(data){
                    if(data.status) obj.onSuccessStatus()
                }
        });
    }
}

let request = new Request('')

class Section{
    constructor(id, url){
        this.id = id
        this.url = url
    }

    getSection(){
        return document.getElementById(this.id)
    }

    render(data){
        let section = this.getSection()
        $(section).html(data);
        $(section).append(data.html);
    }

    request(data=null) {
        let obj = this
        $.ajax({
            async: false,
            url: obj.url,
            data: data,
            type: 'post',
            success: 
                function(render_data){
                    obj.render(render_data)
                }
        });
    }
}

let news_section = new Section('news_section', '')
let one_news_section = new Section('one_news_section', '')
let history_section = new Section('history_section', '')
let users_section = new Section('users_section', '')
let user_section = new Section('user_section', '')
let comments_section = new Section('comments_section', '')
let reviews_section = new Section('reviews_section', '')