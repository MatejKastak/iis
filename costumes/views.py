from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from django.db.utils import IntegrityError
from django.shortcuts import redirect

from .models import *
from .forms import *

def index(request):
    context = {'costumes': Costume.objects, 'accessories': Accessory.objects}
    return render(request, 'costumes/index.html', context)

def costumes(request, costume_id):
    costume = get_object_or_404(Costume, pk=costume_id)
    return render(request, 'costumes/costume.html', {'costume': costume})

def costumes_gallery(request):
    context = {'costumes': Costume.objects}
    return render(request, 'costumes/index.html', context)

def costumes_edit(request, costume_id):
    costume = get_object_or_404(Costume, pk=costume_id)
    if request.method == 'POST':
        form = CostumeForm(request.POST, instance=costume)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/costumes/' + str(costume_id))
    else:
        form = CostumeForm(instance=costume)
            
    return render(request, 'costumes/costume_edit.html', {'form': form, 'costume': costume})

def accessories(request, accessory_id):
    accessory = get_object_or_404(Accessory, pk=accessory_id)
    return render(request, 'costumes/accessory.html', {'accessory': accessory})

def accessories_gallery(request):
    context = {'accessories': Accessory.objects}
    return render(request, 'costumes/index.html', context)

def accessories_edit(request, accessory_id):
    accessory = get_object_or_404(Accessory, pk=accessory_id)
    if request.method == 'POST':
        form = AccessoryForm(request.POST, instance=accessory)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/accessories/' + str(accessory_id))
    else:
        form = AccessoryForm(instance=accessory)
            
    return render(request, 'costumes/accessory_edit.html', {'form': form, 'accessory': accessory})

def basket(request):
    raise Http404('NOT YET IMPLEMENTED')

def login(request):
    return render(request, 'registration/login.html')

def login_script(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            return index(request)
    raise Http404('UNKOWN POST ARGUMENTS FOR THIS REQUEST')

def register(request):
    return render(request, 'registration/sign_up.html')

def register_script(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            if len(form.data['password']) < 6:
                Http404('UNEXPECTED SHORT PASSWORD')
            try:
                user = User.objects.create_user(form.data['login'])
            except IntegrityError:
                return redirect(register)
                return render(request, 'registration/sign_up.html', { "login_exists":True})
            user.first_name = form.data['first_name']
            user.last_name = form.data['last_name']
            user.email = form.data['email']
            user.set_password(form.data['password'])
            user.save()
            return index(request)
    raise Http404('UNKOWN POST ARGUMENTS FOR THIS REQUEST')

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
