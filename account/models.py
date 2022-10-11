from django.db import models

# Create your models here.


class Department(models.Model):
    class Meta:
        db_table = "department"
    id = models.CharField(unique=True, primary_key=True, max_length=10)
    department = models.CharField(unique=True, max_length=50)

    def __str__(self):
        return f"Department  {self.department}"


class Master(models.Model):

    class Meta:
        db_table = "master"
    id = models.CharField(unique=True, primary_key=True, max_length=10)
    initial = models.CharField(max_length=10)
    status =models.CharField(max_length =10, choices = (("Active", "Active"),("Inactive", "Inactive"),))
    def __str__(self):
        return f"Inital : {self.initial}  is {self.status}"


class Employee(models.Model):
    class Meta:
        db_table = 'employee'
    emp_id = models.CharField(primary_key=True, unique=True, max_length=10)
    name = models.CharField("Name", max_length=240)
    emp_department = models.ForeignKey(Department, on_delete=models.CASCADE , related_name='department_name')
    salary = models.FloatField()
    address = models.TextField(max_length=20)
    DOJ = models.DateField("doj", auto_now_add=True)

    def __str__(self):
        return self.name

from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser, AbstractBaseUser

class CURRENT_User(AbstractUser):
    name = models.CharField(max_length=30, default='user')
    phone = models.CharField(max_length=12, default="071234566")
