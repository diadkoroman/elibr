function AdmOptions(){
    var menup = $('#options-menu a')
    var button_sign = 'Додати'
    var addf = $('#add-form')
    var addfbutt = $('#add-form button')
    var addtype=$('input[name=addtype]')
    $('.tab').hide()
    $('.tab').eq(0).show()
    var active_id = $('.tab:eq(0)').attr('id')
    ChangeButton(active_id)
    MakepMenuActive(active_id)
    ManageFields(active_id)

    menup.click(function(){
        active_id = $(this).attr('href').replace('#','')
        ChangeButton(active_id)
        MakepMenuActive(active_id)
        ManageFields(active_id)
        
        $('.tab').hide()
        $('#'+active_id).fadeIn(250)
        })

function ManageFields(active_id){
    $('#add-form p').hide()
    $('#add-form p[class!='+active_id+']').show()
    }

function MakepMenuActive(active_id){
    var active_href='#'+active_id
    $('#options-menu li').removeClass('active')
    $('#options-menu li a[href='+active_href+']').closest('li').addClass('active')
    }

    
        
function ChangeButton(active_id){
    switch(active_id){
        
        case 'books':
        addfbutt.empty().text('Додати книгу')
        addfbutt.attr('type','submit')
        addtype.val(active_id)
        break;
        
        case 'authors':
        addfbutt.empty().text('Додати автора')
        addfbutt.attr('type','submit')
        addtype.val(active_id)
        break;
        
        default:
        addfbutt.attr('type','button')
        addtype.val('')
        break;
        
        }
    }


    var editf = $('#edit-form')
    var editfbutt = $('#edit-form button')
    var active_eid=$('input[name=edittype]').val()
    ChangeButtonEdit(active_eid)
    ManageFieldsEdit(active_eid)
    
    function ChangeButtonEdit(active_eid){
        switch(active_eid){
        
        case 'books':
        editfbutt.empty().text('Редагувати запис(книги)')
        editfbutt.attr('type','submit')
        break;
        
        case 'authors':
        editfbutt.empty().text('Редагувати запис (автори)')
        editfbutt.attr('type','submit')
        break;
        
        default:
        editfbutt.attr('type','button')
        break;
        
        }
    }

function ManageFieldsEdit(active_eid){
    $('#edit-form p').hide()
    $('#edit-form p[class!='+active_eid+']').show()
    }
}
$(document).ready(AdmOptions)
