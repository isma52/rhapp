from django.db import models
#from django_mysql.models import ListCharField
#from django.utils import timezone
from datetime import datetime, date
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from django.core.validators import MinValueValidator, MaxValueValidator

class Employee(models.Model):
    def __str__(self):
        return self.name
    def yearBirthday(self):
        return self.birth_date.year
    def age(self):
        return datetime.today().year - self.birth_date.year
    
    class ProfilTypes(models.TextChoices):
        SB = 'Solution Building', _('SB')
        BA = 'Business Analyst', _('BA')
        PM = 'Project manager', _('PM')
        TE = 'Tester', _('TE')
        PR = 'Production', _('PR')
    employee_number = models.IntegerField(unique=True)
    name = models.CharField(max_length=200)
    surname = models.CharField(max_length=200)
    birth_date = models.DateField(null=True, default =None)
    profil = models.CharField(max_length=50, choices = ProfilTypes.choices, default=ProfilTypes.SB)
    level = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(6)], default = 1)
    maturity = models.CharField(max_length=1, choices = ( ("A","A"), ("B","B") ), default ="A")
    exp_from_date = models.DateField(null=True, default =None)
    company_seniority = models.DateField(null=True, default =None)
    salary = models.IntegerField(null=True, default =None)
    proj = models.ForeignKey('Project',null=True, on_delete=models.SET_DEFAULT, default =None)
    def get_absolute_url(self):
        #return "/employee/%i/" % self.id
        return reverse('employee_detail', args=[str(self.id)])
    

class Crh(models.Model):
    def __str__(self):
        return self.employee.name
    class Meta:
        constraints = [
        models.UniqueConstraint(fields= ['employee','crh_date'], name='unique_crh'),
            ]
    class CrhTypes(models.TextChoices):
        SE = 'SUPERIOR TO EXPECTATIONS', _('SUPERIOR TO EXPECTATIONS')
        AE = 'ABOVE EXPECTATIONS', _('ABOVE EXPECTATIONS')
        ME = 'MEETING EXPECTATIONS', _('MEETING EXPECTATIONS')
        PM = 'PARTIALLY MEETING EXPECTATIONS', _('PARTIALLY MEETING EXPECTATIONS')
        BE = 'BELOW EXPECTATIONS', _('BELOW EXPECTATIONS')
    
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, unique_for_month='crh_date')
    op_perf = models.CharField(max_length=50, choices = CrhTypes.choices, default=CrhTypes.ME)
    crh_date = models.DateField(default=date.today)
    potential = models.CharField(max_length=1, choices = ( ("A","A"), ("B","B"), ("C","C"),("D","D") )
                , default= "C" )
    comment = models.CharField(max_length=400, null=True, default=None)
    #op_perf = ListCharField(base_field=models.CharField(max_length=40))
   
    def month_crh(self):
       return self.crh_date.month
   
    def last_crh(self, arg):
        return self.filter(employee=arg).latest('crh_date')
    
    def get_absolute_url(self):
        #return "/employee/%i/" % self.id
        return reverse('crh_detail', args=[str(self.id)])

class Domain(models.Model):
    def __str__(self):
        return self.name
    name = models.CharField(max_length=200)
    manager = models.ForeignKey(Employee, on_delete=models.SET_DEFAULT, null=True, default =None)
    def get_absolute_url(self):
        #return "/employee/%i/" % self.id
        return reverse('domain_detail', args=[str(self.id)])
    
class Project(models.Model):
    def __str__(self):
        return self.name
    name = models.CharField(max_length=200)
    manager = models.ForeignKey(Employee, on_delete=models.SET_DEFAULT, null=True, default =None)
    domain = models.ForeignKey(Domain, on_delete=models.SET_DEFAULT, null=True, default =None)
    def get_absolute_url(self):
        #return "/employee/%i/" % self.id
        return reverse('project_detail', args=[str(self.id)])
