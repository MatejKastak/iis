from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User, Group, Permission
from django.db.utils import IntegrityError
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, permission_required

from .models import *
from .forms import *

def index(request):
    context = {'costumes': Costume.objects.all(),
               'accessories': Accessory.objects.all(),
               'stores': Store.objects.all(),
               'sizes': Costume.COSTUME_SIZE}
    return render(request, 'costumes/index.html', context)

def costumes(request, costume_id):
    costume = get_object_or_404(Costume, pk=costume_id)
    return render(request, 'costumes/costume.html', {'costume': costume})

def costumes_gallery(request):
    context = {'costumes': Costume.objects.all()}
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
    context = {'accessories': Accessory.objects.all()}
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

def logout_page(request):
    logout(request)
    return HttpResponseRedirect('/gallery')

def login_page(request):
    if "invalid_login" in getMessages(request):
        return render(request, 'registration/login.html', {"invalid_login":True})
    return render(request, 'registration/login.html')

def login_script(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(request, username=form.data['login'], password=form.data['password'])
            if user is None:
                messages.add_message(request, messages.INFO, "invalid_login")
                return HttpResponseRedirect('/login')
            login(request, user)
            return redirect(index)
    raise Http404('UNKOWN POST ARGUMENTS FOR THIS REQUEST')

def register(request):
    if "user_exists" in getMessages(request):
        return render(request, 'registration/sign_up.html', {"user_exists":True})
    return render(request, 'registration/sign_up.html')

def register_script(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            try:
                user = User.objects.create_user(form.data['login'])
            except IntegrityError:
                messages.add_message(request, messages.INFO, "user_exists")
                return HttpResponseRedirect('/register')
            user.first_name = form.data['first_name']
            user.last_name = form.data['last_name']
            user.email = form.data['email']
            user.set_password(form.data['password'])
            user.save()
            group, is_created = Group.objects.get_or_create(name="customers")
            group.user_set.add(user)
            login(request, user)
            return redirect(index)
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
    context = {'stores': Store.objects}
    return render(request, 'costumes/stores.html', context)

def stores(request, store_id):
    store = get_object_or_404(Store, pk=store_id)
    context = {'store': store}
    return render(request, 'costumes/store.html', context)


@login_required(login_url="/login")
@permission_required('costumes.change_employee', raise_exception=True)
def manage_staff(request):
    return render(request, 'manage/manage_staff.html')

def getMessages(request):
    storage = messages.get_messages(request)
    msgs = []
    for msg in messages.get_messages(request):
        msgs.append(str(msg))
    storage.used = True
    return msgs
        
