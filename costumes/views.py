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
from datetime import date

import logging

from .models import *
from .forms import *
from .filters import *

logger = logging.getLogger(__name__)

def index(request):
    context = dict()

    costumes = Costume.objects.none()
    accessories = Accessory.objects.none()

    stores = Store.objects.all()
    stores_checked = dict()
    sizes = Costume.COSTUME_SIZE
    sizes_checked = dict()

    size_q = Q()
    store_q = Q()
    aval_q = Q()
    borrowed_q = Q()

    if request.method == 'GET':

        if not request.GET:

            for size in sizes:
                sizes_checked[size[0]] = 'checked'

            for store in stores:
                stores_checked[store.pk] = 'checked'

            context.update({
                'accessories_checked': 'checked',
                'costumes_checked': 'checked',
                'available_checked': 'checked',
                'borrowed_checked': 'checked',
            })
            costumes = Costume.objects.all()
            accessories = Accessory.objects.all()

        else:

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
                today = date.today()
                if 'aval' in request.GET.getlist('aval') and 'borrowed' in request.GET.getlist('aval'):
                    context['available_checked'] = 'checked'
                    context['borrowed_checked'] = 'checked'
                else:
                    if 'aval' in request.GET.getlist('aval'):
                        context['available_checked'] = 'checked'
                        aval_q = Q(borrowing__return_date__lte=today)
                        costumes = costumes.exclude(borrowing__return_date__gt=today)
                        accessories = accessories.exclude(borrowing__return_date__gt=today)
                    else:
                        context.pop('available_checked', None)

                    if 'borrowed' in request.GET.getlist('aval'):
                        context['borrowed_checked'] = 'checked'
                        borrowed_q = Q(borrowing__return_date__gt=today)
                        costumes = costumes.filter(borrowing__return_date__gt=today)
                        accessories = accessories.filter(borrowing__return_date__gt=today)
                    else:
                        context.pop('borrowed_checked', None)
            else:
                costumes = Costume.objects.none()
                accessories = Accessory.objects.none()

            if request.GET.get('store'):
                store_q = Q(store__pk__in=request.GET.getlist('store'))
                for s in request.GET.getlist('store'):
                    stores_checked[int(s)] = 'checked'

            if request.GET.get('size'):
                size_q = Q(size__in=request.GET.getlist('size'))
                for s in request.GET.getlist('size'):
                    sizes_checked[s] = 'checked'

    costumes = costumes.filter(size_q & store_q)
    accessories = accessories.filter(store_q)

    context.update({'costumes': costumes,
               'accessories': accessories,
               'stores': stores,
               'stores_checked': stores_checked,
               'sizes_checked': sizes_checked,
               'sizes': sizes})
    return render(request, 'costumes/index.html', context)

def costumes(request, costume_id):
    costume = get_object_or_404(Costume, pk=costume_id)
    return render(request, 'costumes/costume.html', {'costume': costume})

@login_required(login_url="/login")
# TODO: @permission_required('costumes.accessories_edit', raise_exception=True)
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

@login_required(login_url="/login")
# TODO: @permission_required('costumes.borrowings_edit', raise_exception=True)
def borrowings_edit(request, borrowing_id):
    borrowing = get_object_or_404(Borrowing, pk=borrowing_id)
    if request.method == 'POST':
        form = BorrowingForm(request.POST, instance=borrowing)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/borrowings/' + str(borrowing_id))
    else:
        form = BorrowingForm(instance=borrowing)

    return render(request, 'costumes/borrowing_edit.html', {'form': form, 'borrowing': borrowing})

@login_required(login_url="/login")
# TODO: @permission_required('costumes.accessories_edit', raise_exception=True)
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

@login_required(login_url="/login")
# TODO: @permission_required('costumes.stores_edit', raise_exception=True)
def stores_edit(request, store_id):
    store = get_object_or_404(Store, pk=store_id)
    if request.method == 'POST':
        form = StoreForm(request.POST, instance=store)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/stores/' + str(store_id))
    else:
        form = StoreForm(instance=store)

    return render(request, 'costumes/store_edit.html', {'form': form, 'store': store})

@login_required(login_url="/login")
# TODO: @permission_required('costume_templates.accessories_edit', raise_exception=True)
def costume_templates_edit(request, costume_template_id):
    costume_template = get_object_or_404(CostumeTemplate, pk=costume_template_id)
    if request.method == 'POST':
        form = CostumeTemplateForm(request.POST, instance=costume_template)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/costume_templates/' + str(costume_template_id))
    else:
        form = CostumeTemplateForm(instance=costume_template)
            
    return render(request, 'costumes/costume_template_edit.html', {'form': form, 'ct': costume_template})

@login_required(login_url="/login")
# TODO: @permission_required('costumes.borrowing_delete', raise_exception=True)
def borrowings_delete(request, borrowing_id):
    # TODO: Maybe add confirmation dialog/ can be js?
    borrowing = get_object_or_404(Borrowing, pk=borrowing_id)
    borrowing.delete()
    return HttpResponseRedirect('/')

@login_required(login_url="/login")
# TODO: @permission_required('costumes.costumes_delete', raise_exception=True)
def costumes_delete(request, costume_id):
    costume = get_object_or_404(Costume, pk=costume_id)
    costume.delete()
    return HttpResponseRedirect('/')

@login_required(login_url="/login")
# TODO: @permission_required('costumes.accessories_delete', raise_exception=True)
def accessories_delete(request, accessory_id):
    accessory = get_object_or_404(Accessory, pk=accessory_id)
    accessory.delete()
    return HttpResponseRedirect('/')

@login_required(login_url="/login")
# TODO: @permission_required('stores.stores_delete', raise_exception=True)
def stores_delete(request, store_id):
    store = get_object_or_404(Store, pk=store_id)
    store.delete()
    return HttpResponseRedirect('/')

@login_required(login_url="/login")
# TODO: @permission_required('costumes.costume_templates_delete', raise_exception=True)
def costume_templates_delete(request, costume_template_id):
    costume_template = get_object_or_404(CostumeTemplate, pk=costume_template_id)
    costume_template.delete()
    return HttpResponseRedirect('/')

def accessories(request, accessory_id):
    accessory = get_object_or_404(Accessory, pk=accessory_id)
    return render(request, 'costumes/accessory.html', {'accessory': accessory})

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


def basket(request):
    costumes = Costume.objects.filter(id__in=request.session['basket_costume'])
    accessory = Accessory.objects.filter(id__in=request.session['basket_accessory'])
    context = {}
    context['costumes'] = costumes
    context['accessory'] = accessory
    if all(c == costumes[0] for c in costumes):
        context['costumes_same_shop'] = True
    if all(c == accessory[0] for c in accessory):
        context['accessory_same_shop'] = True
    if len(costumes) + len(accessory) > 0:
        context['has_items'] = True
    return render(request, 'costumes/basket.html', context)


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
            request.session['basket_costume'] = []
            request.session['basket_accessory'] = []
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
                user = User.objects.create_user(form.data.get('login'))
            except IntegrityError:
                messages.add_message(request, messages.INFO, "user_exists")
                return HttpResponseRedirect('/register')
            user.first_name = form.data.get('first_name')
            user.last_name = form.data.get('last_name')
            user.email = form.data.get('email')
            user.set_password(form.data.get('password'))
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
    # TODO: If user is manager or employee show all of the borrowings
    if True:
        f = BorrowingAdminFilter(request.GET, queryset=Borrowing.objects.all())
    else:
        f = BorrowingUserFilter(request.GET, queryset=Borrowing.objects.filter(customer__user__pk=request.user.pk))

    return render(request, 'costumes/borrowings_gallery.html', {'filter': f})
    
def costume_templates_gallery(request):
    f = CostumeTemplateFilter(request.GET, queryset=CostumeTemplate.objects.all())
    return render(request, 'costumes/costume_templates_gallery.html', {'filter': f})

def borrowings(request, borrowing_id):
    # TODO: Check permissions
    borrowing = get_object_or_404(Borrowing, pk=borrowing_id)
    if not True: # NOT Manager or employee
        # Check if the user has the same pk as the borrowing
        if borrowing.user.pk != borrowing.customer.user.pk:
            pass
    else:
        pass

    context = {'borrowing': borrowing}
    return render(request, 'costumes/borrowing.html', context)

def costume_templates(request, ct_id):
    # TODO: Check permissions
    costume_template = get_object_or_404(CostumeTemplate, pk=ct_id)
    if True: # Manager or employee
        pass
    else:
        # Raise permission error
        pass

    context = {'ct': costume_template}
    return render(request, 'costumes/costume_template.html', context)


def stores_gallery(request):
    context = {'stores': Store.objects}
    return render(request, 'costumes/stores.html', context)

# TODO: Create priviledges 'costumes.costume_add'
class add_costume(LoginRequiredMixin, CreateView):
    login_url = '/login'
    redirect_field_name = '/add_costume'
    model = Costume
    form_class = CostumeForm

# TODO: Create priviledges 'costumes.costume_template_add'
class add_costume_template(LoginRequiredMixin, CreateView):
    login_url = '/login'
    form_class = CostumeTemplateForm
    redirect_field_name = '/add_costume_template'
    model = CostumeTemplate

# TODO: Create priviledges 'costumes.accessory_add'
class add_accessory(LoginRequiredMixin, CreateView):
    login_url = '/login'
    redirect_field_name = '/add_costume'
    model = Accessory
    form_class = AccessoryForm

# TODO: Create priviledges 'stores.store_add'
class add_store(LoginRequiredMixin, CreateView):
    login_url = '/login'
    redirect_field_name = '/add_store'
    model = Store
    form_class = StoreForm

def stores(request, store_id):
    store = get_object_or_404(Store, pk=store_id)
    context = {'store': store}
    return render(request, 'costumes/store.html', context)


@login_required(login_url="/login")
def edit_user(request):
    return render(request, 'registration/edit_user.html')


@login_required(login_url="/login_user")
def edit_user_script(request):
    if request.method == 'POST':
        form = UserEditForm(request.POST)
        if form.is_valid():
            request.user.first_name = form.data.get("first_name")
            request.user.last_name = form.data.get("last_name")
            request.user.email = form.data.get("email")
            request.user.save()
            return redirect(index)
    raise Http404('UNKOWN POST ARGUMENTS FOR THIS REQUEST') 


@login_required(login_url="/login_user")
def change_password(request):
    context = {}
    if "invalid_password" in getMessages(request):
        context["invalid_password"] = True
    return render(request, 'registration/user_change_password.html', context)


@login_required(login_url="/login_user")
def change_password_script(request):
    if request.method == 'POST':
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            user = authenticate(request, username=request.user.username, password=form.data.get('old_password'))
            if user is None:
                messages.add_message(request, messages.INFO, "invalid_password")
                return redirect(change_password)
            else:
                request.user.set_password(form.data.get('new_password'))
                request.user.save()
                return redirect(edit_user)
    raise Http404('UNKOWN POST ARGUMENTS FOR THIS REQUEST') 


@login_required(login_url="/login_user")
def add_costume_to_basket(request):
    if request.method == 'GET':
        if request.GET.get('id'):
            costume_id = int(request.GET.get('id'))
            s = request.session['basket_costume']
            if not costume_id in s:
                s.append(costume_id)
            request.session['basket_costume'] = s
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
        else:
            raise Http404('UNKOWN GET ARGUMENTS FOR THIS REQUEST') 
    raise Http404('EXPECTED GET METHOD') 


@login_required(login_url="/login_user")
def add_accessory_to_basket(request):
    if request.method == 'GET':
        if request.GET.get('id'):
            accessory_id = int(request.GET.get('id'))
            s = request.session['basket_accessory']
            if not accessory_id in s:
                s.append(accessory_id)
            request.session['basket_accessory'] = s
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
        else:
            raise Http404('UNKOWN GET ARGUMENTS FOR THIS REQUEST')
    raise Http404('EXPECTED GET METHOD')


@login_required(login_url="/login_user")
def remove_costume_from_basket(request):
    if request.method == 'GET':
        if request.GET.get('id'):
            costume_id = int(request.GET.get('id'))
            s = request.session['basket_costume']
            s.remove(costume_id)
            request.session['basket_costume'] = s
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
        else:
            raise Http404('UNKOWN GET ARGUMENTS FOR THIS REQUEST')
    raise Http404('EXPECTED GET METHOD')


@login_required(login_url="/login_user")
def remove_accessory_from_basket(request):
    if request.method == 'GET':
        if request.GET.get('id'):
            accessory_id = int(request.GET.get('id'))
            s = request.session['basket_accessory']
            s.remove(accessory_id)
            request.session['basket_accessory'] = s
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
        else:
            raise Http404('UNKOWN GET ARGUMENTS FOR THIS REQUEST')
    raise Http404('EXPECTED GET METHOD')


def getMessages(request):
    storage = messages.get_messages(request)
    msgs = []
    for msg in messages.get_messages(request):
        msgs.append(str(msg))
    storage.used = True
    return msgs
        
