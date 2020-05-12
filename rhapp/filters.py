# -*- coding: utf-8 -*-
"""
Created on Tue Apr 21 18:18:59 2020

@author: iamor
"""

import django_filters

from .models import Employee, Crh, Project, Domain

class ProjectListFilter(django_filters.FilterSet):

    class Meta:
        model = Project
        fields = {'name': ["icontains"], 'domain': ["exact"], 'manager': ["exact"]}
        order_by = ["name"]
 
class DomainListFilter(django_filters.FilterSet):

    class Meta:
        model = Domain
        fields = {'name': ["icontains"], 'manager': ["exact"]}
        order_by = ["name"]
        
class EmployeeListFilter(django_filters.FilterSet):
    #name = django_filters.CharFilter(lookup_expr='iexact')

    class Meta:
        model = Employee
        fields = {'employee_number': ["exact"], 'surname': ["icontains"],'name': ["icontains"], 'profil':["exact"], 'level':["exact"]}
        order_by = ["employee_number"]
        #groups = ['name', 'surname']
        

class CrhListFilter(django_filters.FilterSet):

    #surname = django_filters.ModelChoiceFilter(queryset=Employee.objects.order_by('surname').values('surname'))
    #surname = django_filters.ModelChoiceFilter(queryset=Crh.objects.order_by('employee__name').values('employee__surname'))
    employee =django_filters.ModelChoiceFilter(queryset=Employee.objects.filter(crh__isnull=False).order_by('name').distinct())
    #employee_number = django_filters.ModelChoiceFilter(queryset=Employee.objects.filter(crh__isnull=False).
    #                                           order_by('employee_number').distinct().values_list('employee_number', flat=True),)
    #employee = django_filters.CharFilter(name="employee__name")
    employee_number = django_filters.ModelChoiceFilter(field_name= 'employee__employee_number',
                                               to_field_name='employee_number',
                                               queryset=Employee.objects.filter(crh__isnull=False)
                                               .order_by('employee_number').distinct().values_list('employee_number', flat=True),)
    surname = django_filters.ModelChoiceFilter(field_name= 'employee__surname',
                                               to_field_name='surname',
                                               queryset=Employee.objects.filter(crh__isnull=False)
                                               .order_by('surname').distinct().values_list('surname', flat=True),)
    class Meta:
        model = Crh
        #crh_date = django_filters.DateFromToRangeFilter()
        fields = {'employee_number': ["icontains"], 'employee': ["exact"], 'surname': ["exact"], 'op_perf': ["exact"]}
        order_by = ["employee"]
