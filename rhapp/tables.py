import django_tables2 as tables
from .models import Crh, Employee, Domain, Project
from django.utils import html
from django.utils.translation import gettext_lazy as _

class CrhTable(tables.Table):
    #employee = tables.Column(linkify=True)
    employee_number = tables.Column(verbose_name="Employee number", accessor = "employee__employee_number", 
                             linkify=("employee_detail", (tables.A("employee__id"), )))
    #employee = tables.Column(verbose_name="Employee", accessor = "employee__surname", )
    crh_date = tables.Column(linkify=True, verbose_name = 'Last CRH')
    op_perf = tables.Column(verbose_name = 'Last performance')
    crhHistoric = tables.Column(accessor = "employee__surname", verbose_name="CRH historic", 
                                linkify=("crh_historic", (tables.A("employee__id"), )))
    def render_crhHistoric(self, value, record):
            return html.format_html("<b>{} {}</b>", record.employee, value)
    class Meta:
        model = Crh
        template_name = "django_tables2/bootstrap4.html"
        fields = ( "employee_number", "crhHistoric", "op_perf", "crh_date")
        empty_text = _("No CRH meets the search criteria.")
        
class EmployeeTable(tables.Table):
    emp_to_delete = tables.CheckBoxColumn(accessor='pk',attrs = { "th__input": 
                                        {"onclick": "toggle(this)"}},
                                        orderable=False)
    employee_number = tables.Column(linkify=True, verbose_name = 'Employee number')
    name = tables.Column(verbose_name = 'Name')
    surname = tables.Column(verbose_name = 'Surname')
    age = tables.Column(verbose_name = 'Age')
    profil = tables.Column(verbose_name = 'Profil')
    level = tables.Column(verbose_name = 'Level')
    maturity = tables.Column(verbose_name = 'Maturity')
    #def render_name(self, value, record):
    #        return html.format_html("<b>{} {}</b>", value, record.surname)
    class Meta:
        model = Employee
        template_name = "django_tables2/bootstrap4.html"
        fields = ("emp_to_delete", "employee_number", "name", "surname", "profil",
                  "level", "maturity", "age")
        empty_text = _("No employee meets the search criteria.")
        
class ProjectTable(tables.Table):
    name = tables.Column(linkify=True, verbose_name = 'Name')
    manager = tables.Column(verbose_name = 'Manager')
    domain = tables.Column(verbose_name = 'Domain')
    class Meta:
        model = Project
        template_name = "django_tables2/bootstrap4.html"
        fields = ("name", "domain", "manager")
        empty_text = _("No project meets the search criteria.")
    
class DomainTable(tables.Table):
    name = tables.Column(linkify=True, verbose_name = 'Name')
    manager = tables.Column(verbose_name = 'Manager')
    class Meta:
        model = Domain
        template_name = "django_tables2/bootstrap4.html"
        fields = ("name", "manager")
        empty_text = _("No project meets the search criteria.")