from django.http import Http404
from django.shortcuts import render

def index(request):
    return render(request, 'costumes/index.html')

def costumes(request, costume_id):
    raise Http404('NOT YET IMPLEMENTED')

def costumes_gallery(request):
    raise Http404('NOT YET IMPLEMENTED')

def accessories(request, accessory_id):
    raise Http404('NOT YET IMPLEMENTED')

def accessories_gallery(request):
    raise Http404('NOT YET IMPLEMENTED')

def basket(request):
    raise Http404('NOT YET IMPLEMENTED')

def user(request):
    raise Http404('NOT YET IMPLEMENTED')

def settings(request):
    raise Http404('NOT YET IMPLEMENTED')

def borrowings_gallery(request):
    raise Http404('NOT YET IMPLEMENTED')

def borrowings(request, borrowing_id):
    raise Http404('NOT YET IMPLEMENTED')

def stores_gallery(request):
    raise Http404('NOT YET IMPLEMENTED')

def stores(request, store_id):
    raise Http404('NOT YET IMPLEMENTED')
