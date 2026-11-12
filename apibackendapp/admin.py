from django.contrib import admin
from .models import department,employee,project,userdetails
# from rest_framework.authtoken.models import Token

# Register your models here.

admin.site.register(department)
# admin.site.register(employee)
admin.site.register(project)

#inline class to display many-to-many relationships inside employee admin
class projectinline(admin.TabularInline):
    #tabularinline displays the related data in a table-like format
    #this tells django to use the intermediate(junction) table
    #.through property gives us access to the junction table
    model=project.employees.through
    #mumber of empty rows shown in admin for adding new relationships.
    extra=1

#customizing employee admin panel
class employeeadmin(admin.ModelAdmin):
    #this attaches the inline to employee admin page
    inlines=[projectinline]

#register employee model with customized admin class
admin.site.register(employee,employeeadmin)
# admin.site.register(Token)
admin.site.register(userdetails)