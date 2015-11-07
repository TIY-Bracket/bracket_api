$(document).ready(
    function(){
        $("form").submit(
            function(event){
                event.preventDefault();
                console.log(event);
                var o = {};
                o["Title"] = $(".bracket-title").val();

                var a = [];
                $('.competitor-input').each(
                    function(){
                        a.push({"name": $(this).val()});
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