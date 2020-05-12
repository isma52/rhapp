import pdb
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from .models import Employee, Crh, Project, Domain
from .forms import EmployeeForm, CrhForm, EmployeeFilterFormHelper, CrhFilterFormHelper, UploadFileForm, ProjectForm, DomainForm, ProjectFilterFormHelper, DomainFilterFormHelper
from django.shortcuts import redirect
import copy
from .tables import CrhTable, EmployeeTable, DomainTable, ProjectTable
from .filters import EmployeeListFilter, CrhListFilter, ProjectListFilter, DomainListFilter
from .utils import PagedFilteredTableView, handle_uploaded_file, download_file, webscrap, simple_get
from django.views.generic import View
#from django_tables2 import SingleTableView
 
@method_decorator(login_required, name='dispatch')  
class Crh_list_view(PagedFilteredTableView):
    def lastCRHList(crhEmployeesList):
        lastCRHList = Crh.objects.none()
        for i in crhEmployeesList:
            lastCRHList |= Crh.objects.filter(employee__name=i).order_by('-crh_date')[:1]
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

@method_decorator(login_required, name='dispatch')
class Project_list_view(PagedFilteredTableView):
    model = Project
    table_class = ProjectTable
    filter_class = ProjectListFilter
    template_name = 'rhapp/project_list_view.html'
    formhelper_class = ProjectFilterFormHelper

@method_decorator(login_required, name='dispatch')
class Domain_list_view(PagedFilteredTableView):
    model = Domain
    table_class = DomainTable
    filter_class = DomainListFilter
    template_name = 'rhapp/Domain_list_view.html'
    formhelper_class = DomainFilterFormHelper

@login_required(login_url='/accounts/login/')
def app_list(request):
    return render(request, 'rhapp/app_list.html')

@login_required(login_url='/accounts/login/')
def employee_list(request):
    employees = Employee.objects.filter(birth_date__lte=timezone.now()).order_by('birth_date')
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

def project_new(request):
    if request.method == "POST":
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save()
            return redirect('project_detail', pk=project.pk)
    else:
        form = ProjectForm()
    new = 1
    return render(request, 'rhapp/project_edit.html', {'form': form, 'new': new})

@login_required(login_url='/accounts/login/')
def project_detail(request, pk):
    project = get_object_or_404(Project, pk=pk)
    return render(request, 'rhapp/project_detail.html', {'project': project})


def domain_new(request):
    if request.method == "POST":
        form = DomainForm(request.POST)
        if form.is_valid():
            domain = form.save()
            return redirect('domain_detail', pk=domain.pk)
    else:
        form = DomainForm()
    new = 1
    return render(request, 'rhapp/domain_edit.html', {'form': form, 'new': new})

@login_required(login_url='/accounts/login/')
def domain_detail(request, pk):
    domain = get_object_or_404(Domain, pk=pk)
    page = webscrap()
    page2 = simple_get('https://realpython.com/blog/')
    pdb.set_trace()
    return render(request, 'rhapp/domain_detail.html', {'domain': domain})

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
def project_edit(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if request.method == "POST":
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            project = form.save()
            return redirect('project_detail', pk=project.pk)
    else:
        form = ProjectForm(instance=project)
    new = 0
    return render(request, 'rhapp/project_edit.html', {'form': form, 'new': new, 'project': project})

@login_required(login_url='/accounts/login/')
def project_remove(request, pk):
    project = get_object_or_404(Project, pk=pk)
    project.delete()
    return redirect('/project_list_view')

@login_required(login_url='/accounts/login/')
def domain_edit(request, pk):
    domain = get_object_or_404(Domain, pk=pk)
    if request.method == "POST":
        form = DomainForm(request.POST, instance=domain)
        if form.is_valid():
            domain = form.save()
            return redirect('domain_detail', pk=domain.pk)
    else:
        form = DomainForm(instance=domain)
    new = 0
    return render(request, 'rhapp/domain_edit.html', {'form': form, 'new': new, 'domain': domain})

@login_required(login_url='/accounts/login/')
def domain_remove(request, pk):
    domain = get_object_or_404(Domain, pk=pk)
    domain.delete()
    return redirect('/domain_list_view')

@login_required(login_url='/accounts/login/')
def employee_remove(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    employee.delete()
    return redirect('/employee_list_view')

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
            lastCrh = crhs.filter(employee__name=crh.employee).latest('crh_date')
            crhsLast.append(copy.copy(lastCrh))
        else:
            crhs2 = crhs2.exclude(pk=crh.pk)
    #pdb.set_trace()
    return render(request, 'rhapp/crh_list.html', {'crhsLast': crhsLast})

@login_required(login_url='/accounts/login/')
def crh_detail(request, pk):
    crh = get_object_or_404(Crh, pk=pk)
    emp = Employee.objects.filter(name=crh.employee).distinct().values_list('surname', flat=True)
    return render(request, 'rhapp/crh_detail.html', {'crh': crh, 'emp':emp[0]})

@login_required(login_url='/accounts/login/')
def crh_historic(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    crhs = Crh.objects.filter(employee=employee.pk)
    return render(request, 'rhapp/crh_historic.html', {'crhs': crhs, 'employee':employee})

@login_required(login_url='/accounts/login/')
def employees_upload(request):
    result = "OK"
    remplacement = False
    if request.method == 'POST':
        if 'UploadWithRep' in request.POST:
            remplacement = True
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            for line in request.FILES:
                result = handle_uploaded_file(request.FILES.get(line), remplacement)
            if result != "OK":
                return render(request, 'rhapp/employees_upload.html', {'form': form, 'result': result})
            else:
                return redirect('/employee_list_view')
    else:
        form = UploadFileForm()
    return render(request, 'rhapp/employees_upload.html', {'form': form, 'result': result})

@method_decorator(login_required, name='dispatch')  
class employees_download(View):
    def get(self, request):
        return download_file(Employee)
        