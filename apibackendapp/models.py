from django.db import models
from django.contrib.auth.models import User
#a model is a python class that represents a table in a database
# Create your models here.
class department(models.Model):
    DepartmentId=models.AutoField(primary_key=True)
    DepartmentName=models.CharField(max_length=100)

    def __str__(self):
        return self.DepartmentName

class employee(models.Model):
    EmployeeId=models.AutoField(primary_key=True)
    EmployeeName=models.CharField(max_length=100)
    Designation=models.CharField(max_length=100)
    Dateofjoining=models.DateField()
    DepartmentId=models.ForeignKey(department,on_delete=models.CASCADE)
    contact=models.CharField(max_length=15)
    isactive=models.BooleanField(default=True)

    def __str__(self):
        return self.EmployeeName

class project(models.Model):
    #for many_to_many relationships model,we cannot explicitly define
    #an id field.django will be referring to the default id field
    name=models.CharField(max_length=100,unique=True)
    #define a many to many field
    #related name of this relation will be later referred in the serializer
    employees=models.ManyToManyField(employee,related_name='projects')

    def __str__(self):
        return self.name

class userdetails(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE,related_name='user_details')
    phoneno=models.CharField(max_length=15)
    email=models.EmailField()

    def __str__(self):
        return self.user.username
