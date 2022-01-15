$(document).ready(function () {
    
    var myModal = $('#myModal')

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
            <div class="col-lg-1 pt-1 p-lg-0 col-12">
                <input type="radio" id="primary" name="primary" value="${index}">
                <label for="primary">اصلی</label><br>
            </div>
            <div class="col-6 pt-1 p-lg-0 col-lg-1 my-auto">
                <button class="delete-btn btn btn-outline-danger">حذف</button>
            </div>
        </div>
    </li>`)
        $("#form-address").trigger("reset");
        myModal.modal('hide');
    })


    $(document).on('click', ".delete-btn", function(e) {
        console.log("hazf shod")
        e.preventDefault()
        if ($('.delete-btn').length > 1) {
            $(this).closest($('.li-address')).remove()
            addresses = $(".li-address > div")
            addresses.each(function(index) {
            console.log(index)
                city = $(this).children().eq(0).children().last();
                console.log(city)
                city.attr("name", `address[${index+1}].city`)
                console.log(city.attr("name"))
                street = $(this).children().eq(1).children().last();
                street.attr("name", `address[${index+1}].street`)
                console.log(street.attr("name"))
                plaque = $(this).children().eq(2).children().last();
                plaque.attr("name", `address[${index+1}].plaque`)
                console.log(plaque.attr("name"))
//
                primary = $(this).children().eq(3).children().first();
                primary.val(`${index+1}`)
                console.log(primary.val())

                
              });
        }
        else {
            alert("You must have one address at least!")
        }
    })


     $(document).on('submit','#form-info', function(e){
        e.preventDefault()
        const data = new FormData(e.target);
        const formJSON = Object.fromEntries(data.entries());
        console.log(formJSON["primary"])

        if (formJSON['primary']){

            formJSON['csrfmiddlewaretoken'] = CSRF_TOKEN;
            console.log(formJSON)
            sendAjax(formJSON)
        }
        else {
            alert("ابتدا آدرس اصلی خود را انتخاب کنید.")
        }
         
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