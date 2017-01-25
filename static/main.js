$('document').ready(function(){
    $.ajax({
        method: 'GET',
        url: '/get_open_issues',
        success: function(res){
            for(var k in res){
                $('#openCards').append('<div class="mycards col-md-5">'+res[k].description +'</div>');
            }

        }
    });
});