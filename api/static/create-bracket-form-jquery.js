$(document).ready(
    function(){
        $("form").submit(
            function(){
                var o = {};
                o["Title"] = $(".bracket-title").val();

                var a = [];
                $('.competitor-input').each(
                    function(){
                        a.push({"name": $(this).val()});
                    }
                )

                o["Competitors"] = a;
                $.ajax({
                    url : 'http://127.0.0.1:8000/new_bracket/',
                    method: 'POST',
                    headers: {
                        "Authorization": "Basic " + btoa("admin:password"),
                        "Content-Type": "application/json"
                    },
                    data : JSON.stringify(o)
                })
            }
        );
    }
);
