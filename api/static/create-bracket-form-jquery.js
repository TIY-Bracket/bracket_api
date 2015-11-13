$(document).ready(
    function(){
        $("form").submit(
            function(event){
                event.preventDefault();
                console.log(event);
                var o = {};
                o["Title"] = $(".bracket-title").val();

                var a = [];
                $('.new_competitor').each(
                    function(){
                      console.log($(this).val())
                        // a.push({"name": $(this).val(),
                                // "email":
                      // }
                    // );
                    }
                );

                o["Competitors"] = a;
                $.ajax({
                    url : '/new_bracket/',
                    method: 'POST',
                    headers: {
                        "Authorization": "Basic " + btoa("admin:password"),
                        "Content-Type": "application/json"
                    },
                    data : JSON.stringify(o)
                }).then(
                    function(d){
                        var bracket_id = d['Bracket']
                        console.log(d)
                        window.location = "/view/" + bracket_id;
                    }
                );
            }
        );
    }
);
