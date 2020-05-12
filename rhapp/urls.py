# -*- coding: utf-8 -*-
"""
Created on Mon Apr 13 14:46:00 2020

@author: iamor
"""

from django.urls import path
from . import views
from .views import Crh_list_view, Employee_list_view, Project_list_view, Domain_list_view, employees_download

urlpatterns = [
    path('', views.app_list, name='app_list'),    
    path('employees_list', views.employee_list, name='employee_list'),
    path("employee_list_view", Employee_list_view.as_view()),
    path('employee/<int:pk>/', views.employee_detail, name='employee_detail'),
    path('employee/new/', views.employee_new, name='employee_new'),
    path('employee/<int:pk>/edit/', views.employee_edit, name='employee_edit'),
    path('employee/<pk>/remove_employee/', views.employee_remove, name='employee_remove'),
    path('employees_upload_download', views.employees_upload, name='employees_upload_download'),
    path('employee/remove_employees/', views.employees_remove_from_table, name='employees_remove_from_table'),
    path("employees_download", employees_download.as_view()),
    path('crh_list', views.crh_list, name='crh_list'),
    path("crh_list_view", Crh_list_view.as_view()),
    path('crh/<int:pk>/', views.crh_detail, name='crh_detail'),
    path('crh_historic/<int:pk>/', views.crh_historic, name='crh_historic'),
    path('crh/new/', views.crh_new, name='crh_new'),
    path('crh/<int:pk>/edit/', views.crh_edit, name='crh_edit'),
    path("domain_list_view", Domain_list_view.as_view()),
    path('domain/<int:pk>/', views.domain_detail, name='domain_detail'),
    path('domain/new/', views.domain_new, name='domain_new'),
    path('domain/<int:pk>/edit/', views.domain_edit, name='domain_edit'),
    path('domain/<pk>/remove_domain/', views.domain_remove, name='domain_remove'),
    path("project_list_view", Project_list_view.as_view()),
    path('project/<int:pk>/', views.project_detail, name='project_detail'),
    path('project/new/', views.project_new, name='project_new'),
    path('project/<int:pk>/edit/', views.project_edit, name='project_edit'),
    path('project/<pk>/remove_project/', views.project_remove, name='project_remove'),
]