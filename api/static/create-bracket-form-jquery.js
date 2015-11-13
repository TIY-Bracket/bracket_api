$(document).ready(
    function(){
        $("form").submit(
            function(event){
                event.preventDefault();
                var o = {};
                o["Title"] = $(".bracket-title").val();

                var a = [];
                $('.new_competitor').each(
                    function(){
                      // var name = document.getElementById("comp_name").value;
                      // var email = document.getElementById("comp_email").value;
                      // var phone = document.getElementById("comp_phone").value;
                      var name = $(".comp_name",this).val();
                      var email = $(".comp_email",this).val();
                      var phone = $(".comp_phone",this).val();
                      a.push({"name": name,
                              "email": email,
                              "phone": phone
                      }
                    );
                    }
                );

                o["Competitors"] = a;
                console.log("hereeeee; " + o);
                console.log(JSON.stringify(o))
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
                        window.location = "/view/" + bracket_id;
                    }
                );
            }
        );
    }
);
