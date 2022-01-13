$(document).ready(function () {
    
    var myModal = $('#exampleModal')

    $('.add-address').click(function (e) {
        city = $("#city").val()
        street = $("#street").val()
        plaque = $("#plaque").val()
        index = $("ol").children().length + 1
        $('#form-info div ol').append(`<li class="li-address">
        <div class="address row py-3">
            <div class="col-lg-3 pt-1 p-lg-0 col-12">
                <label for="city-value">شهر:</label>
                <input name="address[${index}].city" id="city-value" type="text"
                       value="${city}">
            </div>

            <div class="col-lg-3 pt-1 p-lg-0 col-12">

                <label for="street-value">خیابان: </label>
                <input name="address[${index}].street" id="street-value" type="text"
                       value="${street}">
            </div>
            <div class="col-lg-3 pt-1 p-lg-0 col-12">
                <label for="plaque-value">پلاک: </label>
                <input name="address[${index}].plaque" id="plaque-value" type="text"
                       value="${plaque}">
            </div>
            <div class="col-6 pt-1 p-lg-0 col-lg-3 my-auto">
                <button class="delete-btn btn btn-outline-danger">حذف</button>
            </div>
        </div>
    </li>`)
        $("#form-address").trigger("reset");
        myModal.modal('hide');
    })


    $(document).on('click', ".delete-btn", function(e) {
        e.preventDefault()
        if ($('.delete-btn').length > 1) {
            $(this).closest($('.li-address')).remove()
        }
        else {
            alert("You must have one address at least!")
        }
    })


     $(document).on('submit','#form-info', function(e){
         e.preventDefault()
         const data = new FormData(e.target);
         const formJSON = Object.fromEntries(data.entries());
         formJSON['csrfmiddlewaretoken'] = CSRF_TOKEN;
         console.log(formJSON)
         sendAjax(formJSON)
    })

    function sendAjax(data) {
        $.ajax({
            type: 'POST',
            url: URL,
            dataType: 'json',
            data: data,
        }).done(function(response){
            alert(response['message']);
        });
    }

})