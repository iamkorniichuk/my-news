class Form extends Section{
    set onSuccessCheck(func){
        this.onSuccess = function(){ func() }
    }

    request(data=null){
        if (data === null) data = {'first_load': true}
        else data['first_load'] = true
        super.request(data)
    }

    check(){
        let obj = this
        let onSuccessStatus = this.onSuccess
        let form = this.getSection().firstElementChild
        console.log(form)
        $.ajax({
            async: false,
            url: obj.url,
            data: new FormData(form),
            processData: false,
            contentType: false,
            type: 'post',
            success: 
                function(data){
                    if(data.html){
                        obj.render(data)
                    }else{
                        form.reset()
                        deletePreviews(form)
                        onSuccessStatus()
                    }
                }
        });
    }
}

let comments_form = new Form('comments_form', '')
let news_form = new Form('news_form', '')
let reviews_form = new Form('reviews_form', '')

class Modal extends Form{
    render(data){
        let section = this.getSection()
        let body = section.getElementsByClassName('modal-body')[0];
        $(body).html(data);
        $(body).append(data.html);
        $(section).modal('show');
    }

    check(){
        let obj = this
        let section = this.getSection()
        let onSuccessStatus = this.onSuccess
        let form = section.getElementsByTagName('form')[0]
        $.ajax({
            async: false,
            url: obj.url,
            data: new FormData(form),
            processData: false,
            contentType: false,
            type: 'post',
            success: 
                function(data){
                    if(data.html){
                        obj.render(data)
                    }else{
                        $(section).modal('hide');
                        onSuccessStatus()
                    }
                }
        });
    }
}

let modal = new Modal('modal', '')