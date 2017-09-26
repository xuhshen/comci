from django.contrib import admin

# Register your models here.
from .models import *


  
class FeatureAdmin(admin.ModelAdmin):  
    filter_horizontal = ('task','module',)  
    
class UserdefcasesetAdmin(admin.ModelAdmin): 
    filter_horizontal = ('caseset',)  


class UserdeftagsetAdmin(admin.ModelAdmin): 
    filter_horizontal = ('tagset',)  

class TaskAdmin(admin.ModelAdmin): 
    filter_horizontal = ('depends',)      
   
admin.site.register(Feature, FeatureAdmin)  

admin.site.register(Featuretype)
admin.site.register(Product)
admin.site.register(Stage)
admin.site.register(Status)
admin.site.register(Gearman)
admin.site.register(Repository)
admin.site.register(Tasktype)
admin.site.register(Task,TaskAdmin)
admin.site.register(Moduletype)
admin.site.register(Module)
admin.site.register(Build)
admin.site.register(Envvariable)
admin.site.register(Caseset)
admin.site.register(Casetag)
admin.site.register(Userdefcaseset,UserdefcasesetAdmin)
admin.site.register(Userdeftagset,UserdeftagsetAdmin)
admin.site.register(Featurebuilder)






