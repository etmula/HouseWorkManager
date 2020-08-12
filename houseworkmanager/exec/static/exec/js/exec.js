$(function(){
class Work{
    constructor(fields){
        this.fields = fields
        this.$work_detail_modal = $('#work-detail-modal');
    }
    

    static bulk_execute(works){
        let data = {'works': []}
        for(let work of works){
            data['works'].push({
                'category': work.fields.category,
                'name': work.fields.name,
                'point': work.fields.point,
                'date': work.fields.date
            })
        }
        $.ajax({
            type: 'post',
            url: '',
            data: JSON.stringify(data),
        })
        .done(function(response){
            $.cookie()
            window.location.href = response;
        });
    };

    static read_fields($element){
        let fields = {
            'id': $element.attr('work-id'),
            'category': $element.attr('category'),
            'name': $element.attr('name'),
            'point': Number($element.attr('point')),
            'description': $element.attr('description'),
            'alert': Number($element.attr('alert')),
            'date': submitter.$datepicker.val()
        };
        return fields
    }
    /*
    show_detail(){
        this.$work_detail_modal.find('.modal-title').html(
            this.fields.name
        );
        let alert_text = this.fields.alert;
        if(isNaN(this.fields.alert)){
            alert_text = 'alertなし'
        }
        this.$work_detail_modal.find('.modal-title').append(
            `<span class="badge badge-info mx-1">${alert_text}</span>`
        );
        this.$work_detail_modal.find('.modal-body').empty();
        this.$work_detail_modal.find('.modal-body').append(`<pre>${this.fields.description}</pre>`);
        this.$work_detail_modal.find('.modal-body').append(`<h5>${this.fields.point}点</h5>`);
        this.$work_detail_modal.modal('show');
    }
    */
}


class Submitter{
    constructor(){
        this.waiting_work_dict = {};
        this.$submit_modal = $('#submit-modal');
        this.$datepicker = $('.datepicker');
        let now = new Date();
        this.$datepicker.datepicker({
            format: "yyyy-mm-dd",
            language: 'ja',
            autoclose: true
        });
        this.$datepicker.datepicker("setDate", now.getFullYear()+now.getMonth+now.getDate());
    }

    waiting_work_dict2works(waiting_work_dict){
        let works = [];
        for(let date in waiting_work_dict){
            for(let id in waiting_work_dict[date]){
                for(let work of waiting_work_dict[date][id]){
                    works.push(work);
                }
            }
        }
        return works;
    }

    rendering_counter(){
        let total_count = 0;
        for(let date in this.waiting_work_dict){
            for(let id in this.waiting_work_dict[date]){
                $(`div[work-id=${id}]`).find('.count-label').text(this.waiting_work_dict[date][id].length)
                total_count += Number(this.waiting_work_dict[date][id].length)
            }
        }
        $('.presubmit-work .badge').text(total_count);
        if(total_count > 0){
            $('.presubmit-work').show();
        }else{
            $('.presubmit-work').hide();
        }
    }

    pre_submit(){
        this.$submit_modal.find('.modal-body').find('.list-group').empty();
        let total_point = 0;

        for(let date in this.waiting_work_dict){
            this.$submit_modal.find('.modal-body').find('.list-group').append(
                `<li class="list-group-item active">
                    ${date}
                </li>`
            );
            for(let id in this.waiting_work_dict[date]){
                for(let work of this.waiting_work_dict[date][id]){
                    this.$submit_modal.find('.modal-body').find('.list-group').append(
                        `<li class="list-group-item">
                            ${work.fields.name}<span class="float-right">${work.fields.point}点</span>
                        </li>`
                    );
                    total_point = total_point + work.fields.point;
                }
            }
        }
        this.$submit_modal.find('.modal-body').find('.list-group').append(
            `<li class="list-group-item text-right">合計: ${total_point}点</li>`
        );
        this.$submit_modal.modal('show');
    };

    submit(){
        $.removeCookie('date')
        $.removeCookie('waiting_work_dict_json')
        let works = this.waiting_work_dict2works(this.waiting_work_dict)
        Work.bulk_execute(works)
        this.$submit_modal.modal('hide');
    };
}

//初期設定
const submitter = new Submitter();
$('.presubmit-work').hide();
let waiting_work_dict_json = $.cookie('waiting_work_dict_json')
if(waiting_work_dict_json !== undefined){
    submitter.waiting_work_dict = JSON.parse(waiting_work_dict_json);
    submitter.rendering_counter();
}

let date = $.cookie('date');
if(date !== undefined){
    submitter.$datepicker.val(date)
}
/*
//仕事詳細表示
$('#main').on('click', '.show-work-modal', function(){
    work = new Work(Work.read_fields($(this).parent()));
    work.show_detail()
});
*/

//日付変更
submitter.$datepicker.on('change', function(){
    $.cookie('date', submitter.$datepicker.val(), {expires: 1/(24*12)});
});

//カウンター
$('.counter').on('click', function(){
    let term = 0;
    let count = $(this).attr('count');
    let work = new Work(Work.read_fields($(this).closest('.work')))
    if(!(work.fields.date in submitter.waiting_work_dict)){submitter.waiting_work_dict[work.fields.date] = {}}
    if(!(work.fields.id in submitter.waiting_work_dict[work.fields.date])){submitter.waiting_work_dict[work.fields.date][work.fields.id] = []}
    if(count == 'up'){
        term = 1;
        submitter.waiting_work_dict[work.fields.date][work.fields.id].push(work)
    }else if(count == 'down'){
        term = -1;
        submitter.waiting_work_dict[work.fields.date][work.fields.id].pop();
    }
    let waiting_work_dict_json = JSON.stringify(submitter.waiting_work_dict);
    $.cookie('waiting_work_dict_json', waiting_work_dict_json, {expires: 7});

    let this_count = Number($(this).parent().find('.count-label').text());
    this_count = Math.max(0, this_count + term);
    $(this).parent().find('.count-label').text(this_count);

    let presubmit_count = 0;
    $('.work .count-label').each(function(index, element){
        presubmit_count = presubmit_count + Number($(element).text());
    });
    $('.presubmit-work .badge').text(presubmit_count);
    if(presubmit_count > 0){
        $('.presubmit-work').show()
    }else{
        $('.presubmit-work').hide()
    }
});

//仕事確認
$('.presubmit-work').on('click', function(){
    submitter.pre_submit(submitter.works)
});

//仕事提出
$('.submit_work').on('click', function(){
    submitter.submit(submitter.works)
});

//categoryフィルター
$('#Category').on('change', function(){
    var category = $(this).val();
    $('.work_item').show();
    if(category != "all"){
        $('.work_info[category!="'+category+'"]').parent().hide();
    }
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


