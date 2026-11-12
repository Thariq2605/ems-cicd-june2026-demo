from rest_framework import serializers
from .models import department,employee,project,userdetails
from datetime import date
import re
from django.contrib.auth.models import User,Group
from django.contrib.auth.hashers import make_password



#validation 1: dataOfjoining current date
#validation 2: employeename should be characters,no special character

#validation of dateofjoining
def date_of_joining_restriction(Dateofjoining):
    today=date.today()
    if Dateofjoining!=today:
        raise serializers.ValidationError("the date ofjoining must be today")
    return Dateofjoining

#validation for employee name
def name_validation(employeename):
    if len(employeename)<3 or not re.match("^[A-za-z]+$",employeename):
        raise serializers.ValidationError("Name must be atleast 3 letters and contain only alphabetic characters")
    return employeename

def designation_validation(Designation):
    if len(Designation) < 2:
        raise serializers.ValidationError(
            "Designation must be at least 2 characters"
        )

    if not re.match("^[A-Za-z ]+$", Designation):
        raise serializers.ValidationError(
            "Designation must contain only alphabets and spaces"
        )

    return Designation

def contact_validation(contact):
    if not re.match("^[0-9]+$", str(contact)):
        raise serializers.ValidationError(
            "Contact must contain only numbers"
        )

    if len(str(contact)) != 10:
        raise serializers.ValidationError(
            "Contact number must contain exactly 10 digits"
        )

    return contact

def isactive_validation(isactive):
    if not isinstance(isactive, bool):
        raise serializers.ValidationError(
            "isactive must be either True or False"
        )

    return isactive

#department serializer
class departmentserializer(serializers.ModelSerializer):
    class Meta:
        model=department
        fields='__all__'


#employee serializer
class employeeserializer(serializers.ModelSerializer):
    Department=departmentserializer(source='DepartmentId',read_only=True)
    Dateofjoining=serializers.DateField(validators=[date_of_joining_restriction])
    EmployeeName=serializers.CharField(max_length=200,validators=[name_validation])
    Designation=serializers.CharField(max_length=100,validators=[designation_validation])
    contact=serializers.IntegerField(validators=[contact_validation])
    isactive=serializers.BooleanField(validators=[isactive_validation])
    #show project details
    project_details=serializers.StringRelatedField(source='projects',many=True,read_only=True)
    class Meta:
        model=employee
        fields=('EmployeeId','EmployeeName','Designation','Dateofjoining',
        'contact','isactive','DepartmentId','Department','project_details',)

class projectserializer(serializers.ModelSerializer):
    #employees--->get the data for employee_details from the employee field of the project model
    employee_details=employeeserializer(source='employees',required=False,many=True,read_only=True)

    class Meta:
        model=project
        fields=('id','name','employees','employee_details')

class userdetailsserializer(serializers.ModelSerializer):
    class Meta:
        model=userdetails
        fields='__all__'

class userserializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=('id','username')

#receives the registration data,validates it and hashes the password,creates the user
#and assigns the user to a group and finally returns the created user
class signupserializer(serializers.ModelSerializer):
    group_name=serializers.CharField(write_only=True,required=False)

    def create(self,validated_data):
        group_name=validated_data.pop("group_name",None)

        #hash the password
        validated_data["password"]=make_password(validated_data.get("password"))

        #create the user
        user=super(signupserializer,self).create(validated_data)

        if group_name:
            group,created=Group.objects.get_or_create(name=group_name)
            user.groups.add(group)
        return user
    class Meta:
        model=User
        fields=["username","password","group_name"]

class loginserializer(serializers.ModelSerializer):
    #field to get username from user
    username=serializers.CharField()
    #field to get password from user
    password=serializers.CharField(write_only=True)

    class Meta:
        model=User
        fields=['username','password']

