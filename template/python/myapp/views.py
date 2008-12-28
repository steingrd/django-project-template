
from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponse

def myapp_index(request):
    return HttpResponse('Hello, myapp')
