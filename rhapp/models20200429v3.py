# -*- coding: utf-8 -*-
from django.db import models
#from django_mysql.models import ListCharField
#from django.utils import timezone
from datetime import datetime, date
from django.utils.translation import gettext_lazy as _
from django.urls import reverse


class Employee(models.Model):
    employee_number = models.IntegerField()
    name = models.CharField(max_length=200)
    surname = models.CharField(max_length=200)
    date_birth = models.DateField()
    def __str__(self):
        return self.name
    def yearBirthday(self):
        return self.date_birth.year
    def age(self):
        return datetime.today().year - self.date_birth.year
    def getName(self):
        return self.name
    def get_absolute_url(self):
        #return "/employee/%i/" % self.id
        return reverse('employee_detail', args=[str(self.id)])
    
    def set_destring_argument(self, argument, value):
        if argument == 'employee_number':
            self.employee_number = value
        elif argument =='name':
            self.name = value
        elif argument == 'surname':
            self.surname = value
        elif argument == 'date_birth':
            self.date_birth = value
        else:
            return False
        return True
        
    
    @classmethod
    def create(cls, employee_data):
        employee = cls(employee_number=employee_data['employee_number'],
                       name=employee_data['name'],
                       surname=employee_data['surname'],
                       date_birth=employee_data['date_birth'],)
        # do something with the book
        return employee

class Crh(models.Model):
    class Meta:
        constraints = [
        models.UniqueConstraint(fields= ['employee','date_crh'], name='unique_crh'),
            ]
    class CrhTypes(models.TextChoices):
        SE = 'SUPERIOR TO EXPECTATIONS', _('SUPERIOR TO EXPECTATIONS')
        AE = 'ABOVE EXPECTATIONS', _('ABOVE EXPECTATIONS')
        ME = 'MEETING EXPECTATIONS', _('MEETING EXPECTATIONS')
        PM = 'PARTIALLY MEETING EXPECTATIONS', _('PARTIALLY MEETING EXPECTATIONS')
        BE = 'BELOW EXPECTATIONS', _('BELOW EXPECTATIONS')
    
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, unique_for_month='date_crh')
    op_perf = models.CharField(max_length=50, choices = CrhTypes.choices, default=CrhTypes.ME)
    date_crh = models.DateField(default=date.today)
    #op_perf = ListCharField(base_field=models.CharField(max_length=40))
    def __str__(self):
        return self.employee.name
   
    def month_crh(self):
       return self.date_crh.month
   
    def last_crh(self, arg):
        return self.filter(employee=arg).latest('date_crh')
    
    def get_absolute_url(self):
        #return "/employee/%i/" % self.id
        return reverse('crh_detail', args=[str(self.id)])
    