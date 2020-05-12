from django import forms

from django.utils.translation import gettext_lazy as _
from crispy_forms.bootstrap import FormActions, InlineField
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Div, Fieldset, Layout, Submit
from bootstrap_datepicker_plus import DatePickerInput

from .models import Employee, Crh, Project, Domain

class EmployeeForm(forms.ModelForm):
    #allow fields not mandatory
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.Meta.not_required:
            self.fields[field].required = False
            
    class Meta:
        model = Employee
        fields = ('employee_number', 'name', 'surname', 'birth_date', 'profil', 'level',
                  'maturity', 'exp_from_date', 'company_seniority', 'salary', 'proj' )
        not_required = ('company_seniority', 'salary', 'proj')
        #https://pypi.org/project/django-bootstrap-datepicker-plus/
        widgets = {
            'birth_date': DatePickerInput(), 'exp_from_date': DatePickerInput(), 
            'company_seniority': DatePickerInput(),
            # default date-format %m/%d/%Y will be used
            #'end_date': DatePickerInput(format='%Y-%m-%d'), # specify date-frmat
        }
        
class CrhForm(forms.ModelForm):

    class Meta:
        model = Crh
        fields = ('employee', 'op_perf', 'crh_date', 'potential', 'comment')
        widgets = {'crh_date': DatePickerInput(),}

class ProjectForm(forms.ModelForm):
    #allow fields not mandatory
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.Meta.not_required:
            self.fields[field].required = False
            
    class Meta:
        model = Project
        fields = ('name', 'manager', 'domain')
        not_required = ('manager', 'domain')
        
class DomainForm(forms.ModelForm):
    #allow fields not mandatory
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.Meta.not_required:
            self.fields[field].required = False
            
    class Meta:
        model = Domain
        fields = ('name', 'manager')
        not_required = ['manager']
        
class EmployeeFilterFormHelper(FormHelper):
    # See https://django-crispy-forms.readthedocs.io/en/latest/form_helper.html

    form_class = "form form-inline"
    form_id = "employee-search-form"
    form_method = "GET"
    form_tag = True
    html5_required = True
    layout = Layout(
        Div(
            Fieldset(
                #str(_("Search employee"))
                "<span class='fa fa-search'></span> " + str(_("")),
                Div(
                    InlineField("employee_number", wrapper_class="col-4"),
                    InlineField("name__icontains", wrapper_class="col-4"),
                    InlineField("surname__icontains", wrapper_class="col-4"),
                    InlineField("profil", wrapper_class="col-4"),
                    InlineField("level", wrapper_class="col-4"),
                    css_class="row",
                ),
                css_class="col-10 border p-3",
            ),
            FormActions(
                Submit("submit", _("Filter")),
                css_class="col-2 text-right align-self-center",
            ),
            css_class="row",
        )
    )
            
class CrhFilterFormHelper(FormHelper):
    # See https://django-crispy-forms.readthedocs.io/en/latest/form_helper.html

    form_class = "form form-inline"
    form_id = "crh-search-form"
    form_method = "GET"
    form_tag = True
    html5_required = True
    layout = Layout(
        Div(
            Fieldset(
                #str(_("Search CRH"))
                "<span class='fa fa-search'></span> " + str(_("")),
                Div(
                    InlineField("employee_number", wrapper_class="col-4"),
                    InlineField("employee", wrapper_class="col-4"),
                    InlineField("surname", wrapper_class="col-4"),
                    InlineField("op_perf", wrapper_class="col-4"),
                    css_class="row",
                ),
                css_class="col-10 border p-3",
            ),
            FormActions(
                Submit("submit", _("Filter")),
                css_class="col-2 text-right align-self-center",
            ),
            css_class="row",
        )
    )

class DomainFilterFormHelper(FormHelper):
    # See https://django-crispy-forms.readthedocs.io/en/latest/form_helper.html

    form_class = "form form-inline"
    form_id = "domain-search-form"
    form_method = "GET"
    form_tag = True
    html5_required = True
    layout = Layout(
        Div(
            Fieldset(
                #str(_("Search domain"))
                "<span class='fa fa-search'></span> " + str(_("")),
                Div(
                    InlineField("name__icontains", wrapper_class="col-4"),
                    InlineField("manager", wrapper_class="col-4"),
                    css_class="row",
                ),
                css_class="col-10 border p-3",
            ),
            FormActions(
                Submit("submit", _("Filter")),
                css_class="col-2 text-right align-self-center",
            ),
            css_class="row",
        )
    )

class ProjectFilterFormHelper(FormHelper):
    # See https://django-crispy-forms.readthedocs.io/en/latest/form_helper.html

    form_class = "form form-inline"
    form_id = "project-search-form"
    form_method = "GET"
    form_tag = True
    html5_required = True
    layout = Layout(
        Div(
            Fieldset(
                #str(_("Search project"))
                "<span class='fa fa-search'></span> " + str(_("")),
                Div(
                    InlineField("name__icontains", wrapper_class="col-4"),
                    InlineField("domain", wrapper_class="col-4"),
                    InlineField("manager", wrapper_class="col-4"),
                    css_class="row",
                ),
                css_class="col-10 border p-3",
            ),
            FormActions(
                Submit("submit", _("Filter")),
                css_class="col-2 text-right align-self-center",
            ),
            css_class="row",
        )
    )
      
            
class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50)
    file = forms.FileField()