$(document).ready(function () {
    $('#checkout-btn').click(function(e){
        if (USER_IS_AUTHENTICATED == "True") {
            $("#addressModal").modal('show')
        } else {
            alert("ابتدا وارد شوید.")
        };
    })

    $("#continue-btn").click(function(e){
        selected_address_index = $('input[type=radio]').index($('input:checked'))
        data = {"selected_address_index": selected_address_index}
        sendAjax(CHECKOUT_URL, data)
    })


    function sendAjax(url, data={}) {
        data['csrfmiddlewaretoken'] = CSRF_TOKEN
        console.log(data)
        $.ajax({
            type: 'POST',
            url: url,
            dataType: 'json',
            data: data,
            success: function(response) {
                reload(response)
            }
        })
    }

    function reload(response) {
        console.log(response)
        $("#addressModal").modal('hide')
        alert(response['message'])
        window.location.reload();
    }
})