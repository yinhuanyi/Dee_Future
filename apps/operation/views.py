from django.shortcuts import render
from django.shortcuts import render_to_response

def page_not_found(request):
    response = render_to_response('operation/404.html', {})
    response.status_code = 404
    return response





def server_error(request):
    response = render_to_response('operation/500.html', {})
    response.status_code = 500
    return response