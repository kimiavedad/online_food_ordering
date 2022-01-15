$(document).ready(function () {
    $('#checkout-btn').click(function(e){
        if (USER_IS_AUTHENTICATED == "True") {
            $("#addressModal").modal('show')
        } else {
            alert("ابتدا وارد شوید.")
        };
    })

    // $("#continue-btn").click(function(e){
        
    //     data = {"selected_address": }

    //     window.location.reload();
    // })


    function sendAjax(url, data={}) {
        data['csrfmiddlewaretoken'] = CSRF_TOKEN
        $.ajax({
            type: 'POST',
            url: url,
            dataType: 'json',
            data: data,
            success: function(response) {
                show_addresses(response)
            }
        })
    }

    function show_addresses(data) {
        if (data["addresses"]) {
            $("#address-body").empty()
            for (const [key, value] of Object.entries(data['addresses'])) {
                console.log(key, value)
                $("#address-body").append()
            }
        }
        
    }

})