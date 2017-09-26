# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User

from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.conf import settings
from rest_framework.fields import empty
import json
from django.db.models import Q

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
        
class Featuretype(models.Model):
    name = models.CharField(max_length=200)
    priority = models.IntegerField(default = 10)
    def __str__(self):
        return self.name 

class Product(models.Model):
    '''define the product ,example:rcp,bts,5g 
    '''
    name = models.CharField(max_length=200)
    
    def __str__(self):
        return self.name

class Stage(models.Model):
    '''define the task phase,in order to run task  serial or parallel
    '''
    name = models.CharField(max_length=200)
    value = models.IntegerField(default=100)
    
    def __str__(self):
        return self.name 

class Key_tables(models.Model):
    key = models.CharField(max_length=200)
    table = models.CharField(max_length=200)
    
    def __str__(self):
        return self.name
    
    def getvalues(self):
        try:
            values = eval(self.table).objects.all()
        except:
            values = None
        
        return values
    
class Status(models.Model):
    '''define the status types for builds and features
    '''
    name = models.CharField(max_length=200)
    def __str__(self):
        return self.name    

class Gearman(models.Model):
    '''define the distribute server,as for different product, this may different
    '''
    name = models.CharField(max_length=200)
    value = models.CharField(max_length=200,default="")
    
    def __str__(self):
        return self.name  

class Repository(models.Model):
    name = models.CharField(max_length=200)
    server = models.CharField(max_length=200)
    
    def __str__(self):
        return self.name  
    
class Tasktype(models.Model):
    '''define the task type ,example: normal task or pipe line or build flow
    '''
    name = models.CharField(max_length=200)
    def __str__(self):
        return self.name
    
class Task(models.Model):
    '''
    '''
    name = models.CharField(max_length=200)
    depends = models.ManyToManyField("self",blank=True) 
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    gearman = models.ForeignKey(Gearman, on_delete=models.CASCADE)
    stage = models.ForeignKey(Stage, on_delete=models.CASCADE)
    type = models.ForeignKey(Tasktype, on_delete=models.CASCADE)
    params = models.TextField(default="",blank=True,help_text='''use to define the task params. one line is one key-value!\n
       var name start with '__' will be reload in feature
       example: key1=value1
                key2=value2
                key3=
                key4=
                __key5=value5
    ''')
    def __str__(self):
        return self.name
    
    def getparams(self):
        res = {}
        for k_val in self.params.split("\n"):
            try:
                clean_str = k_val.strip()
                key,var = clean_str.split("=")
                res[key] = var
            except:
                pass
        return res

class Moduletype(models.Model):
    name = models.CharField(max_length=200)
    def __str__(self):
        return self.name

class Module(models.Model):
    '''define the module of each product,
    '''
    name = models.CharField(max_length=200)
    repository = models.CharField(max_length=200,default="")
    
    type = models.ForeignKey(Moduletype, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    repositoryserver = models.ForeignKey(Repository, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name

class Caseset(models.Model):
    name = models.CharField(max_length=200)
    value = models.CharField(max_length=200)
    
    def __str__(self):
        return self.name

class Userdefcaseset(models.Model):
    name = models.CharField(max_length=200)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    caseset = models.ManyToManyField(Caseset, verbose_name=u'test case set') 
    
    def __str__(self):
        return self.name

class Casetag(models.Model):
    '''define test case tags
    '''
    name = models.CharField(max_length=200)
    tag = models.CharField(max_length=200)
    
    def __str__(self):
        return self.name

class Userdeftagset(models.Model):
    '''define test case tags
    '''
    name = models.CharField(max_length=200)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    tagset = models.ManyToManyField(Casetag, verbose_name=u'test case tag') 
    
    def __str__(self):
        return self.name
    

class Feature(models.Model):
    '''define the feature for product developing
    '''
    name = models.CharField(max_length=200)
    branch = models.CharField(max_length=200,default="")
    featureid = models.CharField(max_length=200,default="")
    
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    type = models.ForeignKey(Featuretype, on_delete=models.CASCADE)
    task = models.ManyToManyField(Task, verbose_name=u'task list') 
    module = models.ManyToManyField(Module, verbose_name=u'subsystem list') 
    
    params = models.TextField(default="",blank=True,help_text="used to redefine task paramers")    
    
    def __str__(self):
        return self.name
    
    def getuser_defined_vars(self):
        vars = []
        for task in self.task.all():
            for k,v in task.getparams().items():
                if k.startswith("__"):
                    name = "{}_{}".format(task.name,k)
                    vars.append({name:v}) 
        return vars 
    
    def getlatestbuild(self):
        return Build.objects.filter(feature__name=self.name)
    
    def getpipeline(self,uuid=None):
        import collections
        pipeline = collections.OrderedDict()
        
        if not uuid:
            tasks = self.task.all()
            stage = set([task.stage.value for task in tasks])
            
            for key in stage:
                pipeline[key] = {}
                
            for task in tasks:
                pipeline[task.stage.value][task.name] = task
        else:
            builds = Build.objects.filter(uuid=uuid)
            stage = set([build.task.stage.value for build in builds])
            
            for key in stage:
                pipeline[key] = {}
                
            for build in builds:
                pipeline[build.task.stage.value][build.name] = build
           
        return pipeline

class Featurebuilder(models.Model):
    name = models.CharField(max_length=200)
    feature = models.ForeignKey(Feature, on_delete=models.CASCADE)
    uuid = models.CharField(max_length=200,default="")

    def __str__(self):
        return "{}_{}".format(self.uuid,self.name)
    
class Build(models.Model):
    '''define the build info for echo task
    '''
    name = models.CharField(max_length=200,default="")
    uuid = models.ForeignKey(Featurebuilder,on_delete=models.CASCADE,blank=True,null=True)
    parent = models.ForeignKey("self", on_delete=models.CASCADE,blank=True,null=True)
    buildurl = models.CharField(max_length=200,default="")
    
    distributor = models.ForeignKey(Gearman, on_delete=models.CASCADE,blank=True,null=True)
    feature = models.ForeignKey(Feature, on_delete=models.CASCADE,blank=True,null=True)
    status = models.ForeignKey(Status, on_delete=models.CASCADE,blank=True,null=True)
    task = models.ForeignKey(Task, on_delete=models.CASCADE,blank=True,null=True)
    trigger = models.ForeignKey(User, on_delete=models.CASCADE,blank=True,null=True)
    params = models.TextField(default="")
    
    def __str__(self):
        return self.name
    
    def getstaticparams(self):
        try:
            res = json.loads(self.params)
        except:
            res = {}
        return res
    
    def getdynamicparams(self):
        res = {}
        #set fixed vars  
        res["CI_BUILD_ID"] = self.id
        res["CI_BUILD_UUID"] = self.uuid.uuid
        res["CI_BUILD_NAME"] = self.name
        res["CI_PRODUCT"] = self.feature.product.name
        res["CI_FEATURENAME"] = self.feature.name
        res["CI_FEATUREBRANCH"] = self.feature.branch
        res["CI_FEATUREID"] = self.feature.featureid
        
        #get global vars from Envvariable table
        result = Envvariable.objects.filter((Q(product__name=self.feature.product)|Q(product__name__isnull=True)),
                                        (Q(task=self.task) | Q(task__isnull=True)))
        for obj in result:
           res[obj.name] = obj.value
        
        # get dynamic vars from feature 
        for k_val in self.feature.params.split("\n"):
            try:
                clean_str = k_val.strip()
                key,var = clean_str.split("=")
                res[key] = var
            except:
                pass
        return res


class Envvariable(models.Model):
    '''define additional environment for testing
       定义变量分几类： 1.对所有产品线所有task生效， 
                2.对某个产品线所有task生效 
                3.对某个task生效
                4.task 级别的变量 分允许重载 和不允许重载
                  对于允许重载的变量，在创建feature的时候，只要添加了这个task，就会自动列出对应的变量
    '''
    product = models.ForeignKey(Product, on_delete=models.CASCADE,null=True,blank=True)
    task = models.ForeignKey(Task, on_delete=models.CASCADE,null=True,blank=True)
    name = models.CharField(max_length=200)
    value = models.CharField(max_length=200)
    
    def __str__(self):
        return self.name

    





    