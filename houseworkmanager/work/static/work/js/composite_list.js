$(function(){
    
    //初期設定
    let $datepicker = $('.datepicker')
    $datepicker.datepicker({
        format: "yyyy-mm-dd",
        language: 'ja',
        autoclose: true
    });
    let date = $.cookie('date');
    if(date){
        $datepicker.val(date)
    }else{
        let now = new Date();
        $datepicker.datepicker("setDate", now.getFullYear()+now.getMonth+now.getDate());
    }

    //日付変更
    $datepicker.on('change', function(){
        $.cookie('date', $datepicker.val(), {expires: 1/(24*12)});
    });

    function submit(work_id, executers, date, $button){
        const wait = (msec)=>{
            return new Promise((resolve)=>{
                setTimeout(()=>{resolve(msec)}, msec);
            });
        };
        console.log(executers)
        let point = $button.text()
        $button.html(`
            <div class="spinner-border spinner-border-sm" role="status">
                <span class="sr-only">Loading...</span>
            </div>
        `)
        $.ajax({
            type:"post",
            url:"/work/work-exected-recodes/create",
            data:JSON.stringify({
                "executers": executers,
                "work": work_id,
                "date": date
            }),
            contentType:'application/json',
            dataType:'json'
        }).done(function(data, textStatus, jqXHR){
            wait(1000).then((waitLength) => {
                $button.text("Done")
            })
        }).fail(function(data, textStatus, jqXHR){
            wait(1000).then((waitLength) => {
                $button.text('Faild')
            })
        })
        wait(1500).then((waitLength) => {
            $button.text(point)
        })

    }
    
    //日付変更
    $datepicker.on('change', function(){
        $.cookie('date', $datepicker.val(), {expires: 1/(24*12)});
    });
    
    //仕事提出
    $('.submit_work').on('click', function(){
        let executers = []
        $("input.executer-checkbox[type='checkbox']:checked").each(function(index, element){
            executers.push($(element).attr('value'))
        });
        submit($(this).attr("work-id"), executers, $datepicker.val(), $(this));
    });
    
    
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = cookies[i].trim();
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    
    //get csrf_token from cookie
    var csrftoken = getCookie('csrftoken');
    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });
    
    });
    
    
    