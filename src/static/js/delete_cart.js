$(document).ready(function () {
    $('.delete-btn').click(function(e){
        index_item = $('.delete-btn').index($(this))
        $(this).closest('tr').remove()
        if ($('.delete-btn').length == 0) {
            $('#cart').empty()
            $('#cart').html('<h1 class="text-center p-4">سبد خرید شما خالیست!</h1>')
        }
        $.ajax({
            type: 'POST',
            url: URL,
            data: {'csrfmiddlewaretoken': CSRF_TOKEN, 'order_item': index_item},
        })
     })
    
})
