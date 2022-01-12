$(document).ready(function() {
    $('.sopt').change(function (e) {
        var optionSelected = $("option:selected", this)
        var text = optionSelected.text();
        this_li = $(this).parent().parent()
        $(this_li).children().eq(1).text('وضعیت: ' + text)
        order_index = $('ol').children().index($(this_li))
        $.ajax({
            type: 'POST',
            url: URL,
            data: {'csrfmiddlewaretoken': CSRF_TOKEN, 'order_index': order_index, 'status': text},
        })
    });
})