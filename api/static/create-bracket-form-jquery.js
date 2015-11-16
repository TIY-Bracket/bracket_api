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
                $.ajaxSetup({
                     beforeSend: function(xhr, settings) {
                         function getCookie(name) {
                             var cookieValue = null;
                             if (document.cookie && document.cookie != '') {
                                 var cookies = document.cookie.split(';');
                                 for (var i = 0; i < cookies.length; i++) {
                                     var cookie = jQuery.trim(cookies[i]);
                                     // Does this cookie string begin with the name we want?
                                     if (cookie.substring(0, name.length + 1) == (name + '=')) {
                                         cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                                         break;
                                     }
                                 }
                             }
                             return cookieValue;
                         }
                         if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
                             // Only send the token to relative URLs i.e. locally.
                             xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
                         }
                     }
                });
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
