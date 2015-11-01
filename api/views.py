from django.http import HttpResponse

# Create your views here.


def hello(request):
    html = """<html>
                <body>
                <h1>Deployment Check</h1>
                <h2>Glenn checking in from Linux.</h2>
                <h2>Glenn checking in from Mac.</h2>
<<<<<<< HEAD
                <h2>Jermaine here</h2>
=======
                <h2>Tyler checking in from Mac.</h2>
>>>>>>> 09b86d12800a773c49463109ba1571935e2d6740
                </body>
            </html>"""
    return HttpResponse(html)
