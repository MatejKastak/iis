from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User, Group, Permission
from django.db.utils import IntegrityError
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView
from django.db.models import Q

import logging

from .models import *
from .forms import *

logger = logging.getLogger(__name__)

def index(request):
    context = dict()

    costumes = Costume.objects.none()
    accessories = Accessory.objects.none()

    stores = Store.objects.all()
    sizes = Costume.COSTUME_SIZE

    size_q = Q()
    store_q = Q()
    aval_q = Q()

    if request.method == 'GET':

        if not request.GET:
            context.update({
                'accessories_checked': 'checked',
                'costumes_checked': 'checked',
                'available_checked': 'checked',
            })
            costumes = Costume.objects.all()
            accessories = Accessory.objects.all()

        if request.GET.get('type'):
            if 'a' in request.GET.getlist('type'):
                accessories = Accessory.objects.all()
                context['accessories_checked'] = 'checked'
            else:
                context.pop('accessories_checked', None)

            if 'c' in request.GET.getlist('type'):
                costumes = Costume.objects.all()
                context['costumes_checked'] = 'checked'
            else:
                context.pop('costumes_checked', None)

        if request.GET.get('aval'):
            if 'aval' in request.GET.getlist('aval'):
                # TODO
                context['available_checked'] = 'checked'
            else:
                context.pop('available_checked', None)

            if 'borrowed' in request.GET.getlist('aval'):
                # TODO
                context['borrowed_checked'] = 'checked'
            else:
                context.pop('borrowed_checked', None)

        if request.GET.get('store'):
            store_q = Q(store__pk__in=request.GET.getlist('store'))

        if request.GET.get('size'):
            size_q = Q(size__in=request.GET.getlist('size'))

    costumes = costumes.filter(size_q & store_q)

    context.update({'costumes': costumes,
               'accessories': accessories,
               'stores': stores,
               'sizes': sizes})
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

def borrowings_edit(request, borrowing_id):
    borrowing = get_object_or_404(Borrowing, pk=borrowing_id)
    if request.method == 'POST':
        form = BorrowingForm(request.POST, instance=borrowing)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/borrowings/' + str(borrowing_id))
    else:
        form = BorrowingForm(instance=borrowing)

    return render(request, 'borrowings/borrowing_edit.html', {'form': form, 'borrowing': borrowing})


def costumes_duplicate(request, costume_id):
    raise Http404('NOT YET IMPLEMENTED')
    costume = get_object_or_404(Costume, pk=costume_id)
    if request.method == 'POST':
        form = CostumeForm(request.POST, instance=costume)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/costumes/' + str(costume_id))
    else:
        form = CostumeForm(instance=costume)

    return render(request, 'costumes/costume_edit.html', {'form': form, 'costume': costume})

def borrowings_delete(request, borrowing_id):
    raise Http404('NOT YET IMPLEMENTED')

def costumes_delete(request, costume_id):
    costume = get_object_or_404(Costume, pk=costume_id)
    costume.delete()
    return HttpResponseRedirect('/')

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

def accessories_duplicate(request, accessory_id):
    raise Http404('NOT YET IMPLEMENTED')
    accessory = get_object_or_404(Accessory, pk=accessory_id)
    if request.method == 'POST':
        form = AccessoryForm(request.POST, instance=accessory)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/accessories/' + str(accessory_id))
    else:
        form = AccessoryForm(instance=accessory)

    return render(request, 'costumes/accessory_edit.html', {'form': form, 'accessory': accessory})

def accessories_delete(request, accessory_id):
    # TODO: Has permission
    accessory = get_object_or_404(Accessory, pk=accessory_id)
    accessory.delete()
    return HttpResponseRedirect('/')

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
            customer = Customer(user=user)
            customer.save()
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
    context = dict()
    if False:
        # TODO: Check if user is employee or manager
        pass
    else:
        context.update({'borrowings': Borrowing.objects.all()})
    return render(request, 'costumes/borrowings.html', context)

def borrowings(request, borrowing_id):
    # TODO: Check permissions
    borrowing = get_object_or_404(Borrowing, pk=borrowing_id)
    context = {'borrowing': borrowing}
    return render(request, 'costumes/borrowing.html', context)

def stores_gallery(request):
    context = {'stores': Store.objects}
    return render(request, 'costumes/stores.html', context)

class add_costume(LoginRequiredMixin, CreateView):
    login_url = '/login'
    redirect_field_name = '/add_costume'
    model = Costume
    fields = '__all__'

class add_costume_template(LoginRequiredMixin, CreateView):
    login_url = '/login'
    form_class = CostumeForm
    redirect_field_name = '/add_costume_template'
    model = CostumeTemplate
    fields = '__all__'

class add_accessory(LoginRequiredMixin, CreateView):
    login_url = '/login'
    redirect_field_name = '/add_costume'
    model = Accessory
    fields = '__all__'

def stores(request, store_id):
    store = get_object_or_404(Store, pk=store_id)
    context = {'store': store}
    return render(request, 'costumes/store.html', context)


@login_required(login_url="/login")
@permission_required('costumes.change_employee', raise_exception=True)
def manage_employee(request):
    context = {'users': User.objects.all()}
    return render(request, 'manage/manage_employee.html', context)


@login_required(login_url="/login")
@permission_required('costumes.change_manager', raise_exception=True)
def manage_manager(request):
    context = {'users': User.objects.all()}
    return render(request, 'manage/manage_manager.html', context)


@login_required(login_url="/login")
@permission_required('costumes.change_manager', raise_exception=True)
def edit_manager(request, manager_id):
    context = {}
    context['manager'] = User.objects.get(pk=manager_id)
    context['store'] = Store.objects.all()
    return render(request, 'manage/edit_manager.html', context)


@login_required(login_url="/login")
@permission_required('costumes.change_manager', raise_exception=True)
def edit_manager_script(request):
    if request.method == 'POST':
        form = EditManagerForm(request.POST)
        if form.is_valid():
            u = User.objects.get(id=int(form.data.get('id')))
            m = Manager.objects.get(user=u)
            u.first_name = form.data.get('first_name')
            u.last_name = form.data.get('last_name')
            u.email = form.data.get('email')
            m.address = form.data.get('address')
            m.tel_num = form.data.get('tel_num')
            if form.data.get('store'):
                m.store = int(form.data.get('store'))
            u.save()
            m.save()
            return redirect(manage_manager)
    raise Http404('UNKOWN POST ARGUMENTS FOR THIS REQUEST')


def getMessages(request):
    storage = messages.get_messages(request)
    msgs = []
    for msg in messages.get_messages(request):
        msgs.append(str(msg))
    storage.used = True
    return msgs
        
