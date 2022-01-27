$(document).ready(function () {

    $('#search-btn').click(function(e){
        console.log('hii')
        $.ajax({
            type: 'POST',
            url: URL_SEARCH,
            data: {'csrfmiddlewaretoken': CSRF_TOKEN, 'searched_content': $("#search-input").val()},
            success: function(response) {
                show_items(response)
            }
        })
        $('#exampleModal').modal('show')
     });

    
    function show_items(data){
        $("#search-body").empty()
        console.log(data['object_list'])
        if (data['object_list']){
            for (const [key, value] of Object.entries(data['object_list'])) {
                if (data['type']=='food') {
                    $("#search-body").append(`
                    <a class="text-decoration-none" href="http://CustomUser.0.0.1:8000/food/${value['pk']}">
                        <h5>${value['food__name']}</h5>
                    </a>
                    <div class="row">
                        <div class="col text-muted"> رستوران ${value['branch__restaurant__name']} ${value['branch__name']}</div>
                    </div>
                    <hr>`)

                    if (USER_IS_ADMIN  === "True") {
                        tag_a = $("#search-body").children("a").last()
                        $(tag_a).attr('href', `http:/\/CustomUser.0.0.1:8000/site_admin/food/${value['pk']}/edit/`)
                    }
                }
//              if data["type"] == 'restaurant'
                else {
                    $("#search-body").append(`
                    <a class="text-decoration-none" href="http://127.0.0.1:8000/restaurant/${value['pk']}/">
                        <h5> رستوران ${value['restaurant__name']} ${value['name']}</h5></a><hr>`)
                }
            }
        }
        else{
            $("#search-body").append(`<h5>${data['message']}</h5>`)
        }

    };

})