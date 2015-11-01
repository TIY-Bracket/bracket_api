from django.http import HttpResponse

# Create your views here.


def hello(request):
    html = """<html>
                <body>
                <h1>Deployment Check</h1>
                <h2>Glenn checking in from Linux.</h2>
                <h2>Glenn checking in from Mac.</h2>
                <h2>Jermaine checking in from Mac.</h2>
                <h2>Tyler checking in from Mac.</h2>
                </body>
            </html>"""
    return HttpResponse(html)
