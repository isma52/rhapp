import pdb
#from django.views.generic import ListView
#from django_filters.views import FilterView
#from django.db.models import Count, Max
#from django_tables2 import SingleTableView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from .models import Employee, Crh
from .forms import EmployeeForm, CrhForm, EmployeeFilterFormHelper, CrhFilterFormHelper, UploadFileForm
from django.shortcuts import redirect
import copy
from .tables import CrhTable, EmployeeTable
from .filters import EmployeeListFilter, CrhListFilter
from .utils import PagedFilteredTableView, handle_uploaded_file
import pandas as pd
from xlrd import XLRDError
 
@method_decorator(login_required, name='dispatch')  
class Crh_list_view(PagedFilteredTableView):
    def lastCRHList(crhEmployeesList):
        lastCRHList = Crh.objects.none()
        for i in crhEmployeesList:
            lastCRHList |= Crh.objects.filter(employee__name=i).order_by('-date_crh')[:1]
        return lastCRHList
    model = Crh
    filter_class = CrhListFilter
    crhEmployeesList = Crh.objects.order_by().values_list('employee__name', flat=True).distinct()
    queryset = lastCRHList(crhEmployeesList)
    table_class = CrhTable
    template_name = 'rhapp/crh_list_view.html'
    formhelper_class = CrhFilterFormHelper

@method_decorator(login_required, name='dispatch')
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
            emp.delete()
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

def employees_upload(request):
    result = "OK"
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            for line in request.FILES:
                result = handle_uploaded_file(request.FILES.get(line))
            if result != "OK":
                return render(request, 'rhapp/employees_upload.html', {'form': form, 'result': result})
            else:
                return redirect('/employee_list_view')
    else:
        form = UploadFileForm()
    return render(request, 'rhapp/employees_upload.html', {'form': form, 'result': result})

def handle_uploaded_fileee(f):
    sheetNameData = 'Data'
    name = 'Prénom'
    surname = 'Nom'
    date_birth = 'Date naissance'
    employee_number = 'Matricule'
    result = "OK"
    fileData = []
    try:
        fileData = pd.read_excel(f,  sheet_name=sheetNameData,skiprows=1)
        employeeArguments = []
        if (surname and name and date_birth and employee_number) in fileData:
            #TO DO: catch error if argument not in Excel
            employeeArguments = [surname, name, date_birth, employee_number]
            d = {'name':['Prénom'],'surname':['Nom'], 'date_birth':['Date naissance'], 'employee_number':['Matricule']}
            df = pd.DataFrame(data=d)
            dataToSave = fileData[employeeArguments]
            employeesSaved = 0
            for i in dataToSave.index:
                employeeToSave = Employee()
                for e in df:
                    setattr(employeeToSave,e, dataToSave[df[e][0]][i])
                employeeToSave.save()
                employeesSaved += 1
        print("employeesSaved")
        print(print(employeesSaved))
    except XLRDError:
        print("format error")
        result = "The file selected have not the right Excel format (xls or xlsx)"
    except TypeError as e:
        result = "Some values have not the right type: "+ str(e)
    except Exception as e:
        result = "An error occured when uploading the file: "+ str(e)
    finally:
        return result
        
        