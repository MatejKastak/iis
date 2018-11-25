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

from .models import Store, Employee, Manager
from .forms import EditEmployeeForm, CreateEmployeeForm, CreateManagerForm, EditManagerForm
from .views import getMessages


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
    for g in User.objects.get(pk=manager_id).groups.all():
        if g.name == "super_manager":
            context['is_super_manager'] = True
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
                s = Store.objects.get(id=int(form.data.get('store')))
                m.store = s
            if form.data.get('super_manager'):
                g = Group.objects.get(name="super_manager")
                g.user_set.add(u)
                g.save()
            else:
                for g in u.groups.all():
                    if g.name == "super_manager":
                        u.groups.remove(g)
                        break
            u.save()
            m.save()
            return redirect(manage_manager)
    raise Http404('UNKOWN POST ARGUMENTS FOR THIS REQUEST')


@login_required(login_url="/login")
@permission_required('costumes.add_manager', raise_exception=True)
def create_manager(request):
    context = {}
    if "manager_exists" in getMessages(request):
        context['manager_exists'] = True
    context['store'] = Store.objects.all()
    return render(request, 'manage/create_manager.html', context)


@login_required(login_url="/login")
@permission_required('costumes.add_manager', raise_exception=True)
def create_manager_script(request):
    if request.method == 'POST':
        form = CreateManagerForm(request.POST)
        if form.is_valid():
            try:
                u = User.objects.create_user(form.data['login'])
            except IntegrityError:
                messages.add_message(request, messages.INFO, "manager_exists")
                return redirect(create_manager)
            u.set_password(form.data.get("password"))
            u.first_name = form.data.get("first_name")
            u.last_name = form.data.get("last_name")
            u.email_name = form.data.get("email_name")
            u.save()
            m = Manager.objects.create(user=u)
            m.address = form.data.get("address")
            m.tel_num = form.data.get("tel_num")
            m.store
            if form.data.get('store'):
                s = Store.objects.get(id=int(form.data.get('store')))
                m.store = s
            m.save()
            g = Group.objects.get(name="manager")
            g.user_set.add(u)
            g.save()
            if form.data.get('super_manager'):
                g = Group.objects.get(name="super_manager")
                g.user_set.add(u)
                g.save()
            return redirect(manage_manager)
    raise Http404('UNKOWN POST ARGUMENTS FOR THIS REQUEST')


@login_required(login_url="/login")
@permission_required('costumes.delete_manager', raise_exception=True)
def delete_manager(request):
    if request.GET.get("id"):
        u = User.objects.get(id=int(request.GET.get("id")))
        u.delete()
        return redirect(manage_manager)
    return Http404('UNKOWN GET ARGUMENTS FOR THIS REQUEST')


@login_required(login_url="/login")
@permission_required('costumes.change_employee', raise_exception=True)
def edit_employee(request, employee_id):
    context = {}
    context['employee'] = User.objects.get(pk=employee_id)
    context['store'] = Store.objects.all()
    return render(request, 'manage/edit_employee.html', context)


@login_required(login_url="/login")
@permission_required('costumes.change_employee', raise_exception=True)
def edit_employee_script(request):
    if request.method == 'POST':
        form = EditEmployeeForm(request.POST)
        if form.is_valid():
            u = User.objects.get(id=int(form.data.get('id')))
            m = Employee.objects.get(user=u)
            u.first_name = form.data.get('first_name')
            u.last_name = form.data.get('last_name')
            u.email = form.data.get('email')
            m.address = form.data.get('address')
            m.tel_num = form.data.get('tel_num')
            if form.data.get('store'):
                s = Store.objects.get(id=int(form.data.get('store')))
                m.store = s
            u.save()
            m.save()
            return redirect(manage_employee)
    raise Http404('UNKOWN POST ARGUMENTS FOR THIS REQUEST')


@login_required(login_url="/login")
@permission_required('costumes.add_employee', raise_exception=True)
def create_employee(request):
    context = {}
    if "employee_exists" in getMessages(request):
        context['employee_exists'] = True
    context['store'] = Store.objects.all()
    return render(request, 'manage/create_employee.html', context)


@login_required(login_url="/login")
@permission_required('costumes.add_employee', raise_exception=True)
def create_employee_script(request):
    if request.method == 'POST':
        form = CreateEmployeeForm(request.POST)
        if form.is_valid():
            try:
                u = User.objects.create_user(form.data['login'])
            except IntegrityError:
                messages.add_message(request, messages.INFO, "employee_exists")
                return redirect(create_employee)
            u.set_password(form.data.get("password"))
            u.first_name = form.data.get("first_name")
            u.last_name = form.data.get("last_name")
            u.email_name = form.data.get("email_name")
            u.save()
            m = Employee.objects.create(user=u)
            m.address = form.data.get("address")
            m.tel_num = form.data.get("tel_num")
            m.store
            if form.data.get('store'):
                s = Store.objects.get(id=int(form.data.get('store')))
                m.store = s
            m.save()
            g = Group.objects.get(name="employee")
            g.user_set.add(u)
            g.save()
            return redirect(manage_employee)
    raise Http404('UNKOWN POST ARGUMENTS FOR THIS REQUEST')


@login_required(login_url="/login")
@permission_required('costumes.delete_employee', raise_exception=True)
def delete_employee(request):
    if request.GET.get("id"):
        u = User.objects.get(id=int(request.GET.get("id")))
        u.delete()
        return redirect(manage_employee)
    return Http404('UNKOWN GET ARGUMENTS FOR THIS REQUEST')
