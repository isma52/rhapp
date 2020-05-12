import pdb
#from django.views.generic import ListView
#from django_filters.views import FilterView
#from django.db.models import Count, Max
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from .models import Employee, Crh
from .forms import EmployeeForm, CrhForm, EmployeeFilterFormHelper
from django.shortcuts import redirect
import copy
from django_tables2 import SingleTableView
from .tables import CrhTable, EmployeeTable
from .filters import EmployeeListFilter
from .utils import PagedFilteredTableView

    
class Crh_list_view(SingleTableView):
    #crhs = Crh.objects.order_by('date_crh').values_list('employee', flat=True).distinct()
    #crhs = Crh.objects.latest('date_crh')
    #crhs = Crh.objects.order_by('date_crh').values_list('employee', flat=True).distinct()
    #orderedList = Crh.objects.order_by('-date_crh')
    #duplicateList = orderedList.annotate(max_id=Max('employee'), count_id=Count('employee')).filter(count_id__gt=1)
    #id_list = Crh.objects.order_by('date_crh').values_list('employee', flat= True).distinct()
    #idd = Crh.objects.values_list('employee').order_by('-date_crh').values_list('employee')
    def lastCRHList(crhEmployeesList):
        lastCRHList = Crh.objects.none()
        for i in crhEmployeesList:
            lastCRHList |= Crh.objects.filter(employee__name=i).order_by('-date_crh')[:1]
        return lastCRHList
    model = Crh
    crhEmployeesList = Crh.objects.order_by().values_list('employee__name', flat=True).distinct()
    queryset = lastCRHList(crhEmployeesList)
    table_class = CrhTable
    template_name = 'rhapp/crh_list_view.html'

class Employee_list_view(PagedFilteredTableView):
    model = Employee
    table_class = EmployeeTable
    filter_class = EmployeeListFilter
    template_name = 'rhapp/employee_list_view.html'
    formhelper_class = EmployeeFilterFormHelper
    


@login_required(login_url='/accounts/login/')
def app_list(request):
    return render(request, 'rhapp/app_list.html')

@login_required(login_url='/accounts/login/')
def employee_list(request):
    employees = Employee.objects.filter(date_birth__lte=timezone.now()).order_by('date_birth')
    return render(request, 'rhapp/employee_list.html', {'employees': employees})

@login_required(login_url='/accounts/login/')
def employee_detail(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    return render(request, 'rhapp/employee_detail.html', {'employee': employee})

@login_required(login_url='/accounts/login/')
def employee_new(request):
    if request.method == "POST":
        form = EmployeeForm(request.POST)
        if form.is_valid():
            employee = form.save()
            return redirect('employee_detail', pk=employee.pk)
    else:
        form = EmployeeForm()
    new = 1
    return render(request, 'rhapp/employee_edit.html', {'form': form, 'new': new})

@login_required(login_url='/accounts/login/')
def crh_new(request):
    if request.method == "POST":
        form = CrhForm(request.POST)
        if form.is_valid():
            crh = form.save()
            return redirect('crh_detail', pk=crh.pk)
    else:
        form = CrhForm()
    new = 1
    return render(request, 'rhapp/crh_edit.html', {'form': form, 'new': new})

@login_required(login_url='/accounts/login/')
def crh_edit(request, pk):
    crh = get_object_or_404(Crh, pk=pk)
    if request.method == "POST":
        form = CrhForm(request.POST, instance=crh)
        if form.is_valid():
            crh = form.save()
            return redirect('crh_detail', pk=crh.pk)
    else:
        form = CrhForm(instance=crh)
    new = 0
    return render(request, 'rhapp/crh_edit.html', {'form': form, 'new': new, 'crh': crh})

@login_required(login_url='/accounts/login/')
def crh_remove(request, pk):
    crh = get_object_or_404(Crh, pk=pk)
    crh.delete()
    return redirect('crh_list_view')

@login_required(login_url='/accounts/login/')
def employee_edit(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    if request.method == "POST":
        form = EmployeeForm(request.POST, instance=employee)
        if form.is_valid():
            employee = form.save()
            return redirect('employee_detail', pk=employee.pk)
    else:
        form = EmployeeForm(instance=employee)
    new = 0
    return render(request, 'rhapp/employee_edit.html', {'form': form, 'new': new, 'employee': employee})

@login_required(login_url='/accounts/login/')
def employee_remove(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    employee.delete()
    return redirect('employee_list_view')

@login_required(login_url='/accounts/login/')
def employees_remove_from_table(request):
    if request.method == "POST":
        pks = request.POST.getlist("emp_to_delete")
        employees = Employee.objects.filter(pk__in=pks)
        for emp in employees:
            #emp.delete()
            print(emp)
    return redirect('/employee_list_view')

@login_required(login_url='/accounts/login/')
def crh_list(request):
    crhs = Crh.objects.order_by('employee')
    crhsLast = []
    crhs2 = Crh.objects.order_by('employee')
    for crh in crhs:
        if crh not in crhsLast:
            lastCrh = crhs.filter(employee__name=crh.employee).latest('date_crh')
            crhsLast.append(copy.copy(lastCrh))
        else:
            crhs2 = crhs2.exclude(pk=crh.pk)
    #pdb.set_trace()
    return render(request, 'rhapp/crh_list.html', {'crhsLast': crhsLast})

@login_required(login_url='/accounts/login/')
def crh_detail(request, pk):
    crh = get_object_or_404(Crh, pk=pk)
    return render(request, 'rhapp/crh_detail.html', {'crh': crh})

@login_required(login_url='/accounts/login/')
def crh_historic(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    crhs = Crh.objects.filter(employee=employee.pk)
    return render(request, 'rhapp/crh_historic.html', {'crhs': crhs})