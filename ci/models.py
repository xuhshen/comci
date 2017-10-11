# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User

from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.conf import settings
from rest_framework.fields import empty
import json
import collections
from django.db.models import Q

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
        
class Featuretype(models.Model):
    name = models.CharField(max_length=200)
    priority = models.IntegerField(default = 10)
    create_time = models.DateTimeField(auto_now_add=True)
    lastupdate_time = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.name 
    
    def getvalue(self):
        return self.name

class Product(models.Model):
    '''define the product ,example:rcp,bts,5g 
    '''
    name = models.CharField(max_length=200)
    create_time = models.DateTimeField(auto_now_add=True)
    lastupdate_time = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    def getvalue(self):
        return self.name
    
class Stage(models.Model):
    '''define the task phase,in order to run task  serial or parallel
    '''
    name = models.CharField(max_length=200)
    value = models.IntegerField(default=100)
    create_time = models.DateTimeField(auto_now_add=True)
    lastupdate_time = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name 
    
    def getvalue(self):
        return self.name

class Status(models.Model):
    '''define the status types for builds and features
    '''
    name = models.CharField(max_length=200)
    create_time = models.DateTimeField(auto_now_add=True)
    lastupdate_time = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.name  
    
    def getvalue(self):
        return self.name  

class Gearman(models.Model):
    '''define the distribute server,as for different product, this may different
    '''
    name = models.CharField(max_length=200)
    value = models.CharField(max_length=200,default="")
    create_time = models.DateTimeField(auto_now_add=True)
    lastupdate_time = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name  
    
    def getvalue(self):
        return self.name

class Repository(models.Model):
    name = models.CharField(max_length=200)
    server = models.CharField(max_length=200)
    create_time = models.DateTimeField(auto_now_add=True)
    lastupdate_time = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name  
    
    def getvalue(self):
        return self.name
    
class Tasktype(models.Model):
    '''define the task type ,example: normal task or pipe line or build flow
    '''
    name = models.CharField(max_length=200)
    create_time = models.DateTimeField(auto_now_add=True)
    lastupdate_time = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.name
    
    def getvalue(self):
        return self.name

class TaskParam(models.Model):
    name = models.CharField(max_length=200)
    value = models.CharField(max_length=200)
    
    def __str__(self):
        pass
    
    def getvalue(self):
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
    create_time = models.DateTimeField(auto_now_add=True)
    lastupdate_time = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    def getcustomparams(self,):
        membertable = "Key_tables"
        bound_vars = {var.key:var for var in eval(membertable).objects.filter(task=self)}

        res = {}
        for k_val in self.params.split("\n"):
            try:
                clean_str = k_val.strip()
                key,var = clean_str.split("=")
                if key.startswith("**"):
                    n_key = key.replace("**","") 
                    if bound_vars.has_key(n_key):
                        res[n_key] = bound_vars[n_key].getvalue()
                    else:
                        res[n_key] = var
            except:
                pass
            
        return res
 
class FilterTables(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Key_tables(models.Model):
    key = models.CharField(max_length=200)
    table = models.ForeignKey(FilterTables, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    
    create_time = models.DateTimeField(auto_now_add=True)
    lastupdate_time = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.key
    
    def getvaluelist(self):
        try:
            values = eval(self.table.name).objects.all()
        except:
            return None
        return values
    
    def getvalue(self):
        try:
            val = self.getvaluelist()[0].getvalue()
        except:
            val = ""
            
        return val

class Moduletype(models.Model):
    name = models.CharField(max_length=200)
    create_time = models.DateTimeField(auto_now_add=True)
    lastupdate_time = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    def getvalue(self):
        return self.name

class Module(models.Model):
    '''define the module of each product,
    '''
    name = models.CharField(max_length=200)
    repository = models.CharField(max_length=200,default="")
    
    type = models.ForeignKey(Moduletype, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    repositoryserver = models.ForeignKey(Repository, on_delete=models.CASCADE)
    create_time = models.DateTimeField(auto_now_add=True)
    lastupdate_time = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name

    def getvalue(self):
        return self.name
    
class Caseset(models.Model):
    name = models.CharField(max_length=200)
    value = models.CharField(max_length=200)
    create_time = models.DateTimeField(auto_now_add=True)
    lastupdate_time = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    def getvalue(self):
        return self.value

class Userdefcaseset(models.Model):
    name = models.CharField(max_length=200)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    caseset = models.ManyToManyField(Caseset, verbose_name=u'test case set') 
    
    create_time = models.DateTimeField(auto_now_add=True)
    lastupdate_time = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.name
    
    def getvalue(self):
        res = [item.getvalue() for item in self.caseset.all()]
        return res

class Casetag(models.Model):
    '''define test case tags
    '''
    name = models.CharField(max_length=200)
    tag = models.CharField(max_length=200)
    
    create_time = models.DateTimeField(auto_now_add=True)
    lastupdate_time = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    def getvalue(self):
        return self.tag
    
    
class Userdeftagset(models.Model):
    '''define test case tags
    '''
    name = models.CharField(max_length=200)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    tagset = models.ManyToManyField(Casetag, verbose_name=u'test case tag') 
    create_time = models.DateTimeField(auto_now_add=True)
    lastupdate_time = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name

    def getvalue(self):
        res = [item.getvalue() for item in self.tagset.all()]
        return res
    
class Param(models.Model):
    name = models.CharField(max_length=200)
    value = models.CharField(max_length=500)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name
    
    def getboundtable(self):
        try:
            bound_table = Key_tables.objects.get(task=self.task,key=self.name).table.name
        except:
            bound_table = ""
        return bound_table
    
    def getdefaultvalue(self):
        table = self.getboundtable()
        if table:
            lst = {item.id:[item.name,item.value] for item in eval(table).objects.all()}
        else:
            lst = {}
        return lst
    
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
    
#     params = models.TextField(default="",blank=True,help_text="used to redefine task paramers")    
    params = models.ManyToManyField(Param, verbose_name=u'Params') 
    
    create_time = models.DateTimeField(auto_now_add=True)
    lastupdate_time = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    def getcurrent_vars(self):
        res = collections.OrderedDict({ 
                    task.name:
                        {
                         p.name:{"value":p.value,
                                 "table":p.getboundtable()
                                 } 
                           for p in self.params.filter(task=task) 
                        } 
                    for task in self.task.all()
                  })
        return res
    
    def updateparams(self,res,task,add=True):
        if add:
            if not res.has_key(task.name):
                res[task.name] = task.getfeature_defined_params()
        else:
            try:del res[task.name]
            except:pass
        return res
        
    def getlatestbuild(self):
        '''manytomany field'''
        return Build.objects.filter(feature__name=self.name)
    
    def getpipeline(self,uuid=None):
        pipeline = collections.OrderedDict()
        
        if not uuid:
            tasks = self.task.all()
            stage = sorted(list(set([task.stage.value for task in tasks])))
            
            for key in stage:
                pipeline[key] = {}
                
            for task in tasks:
                pipeline[task.stage.value][task.name] = task
        else:
            builds = Build.objects.filter(uuid=uuid)
            stage = sorted(list(set([build.task.stage.value for build in builds])))
            
            for key in stage:
                pipeline[key] = {}
                
            for build in builds:
                pipeline[build.task.stage.value][build.name] = build
        return pipeline
    
    def getlatestpipeline(self):
        try:
            latestbuild = Featurebuilder.objects.order_by('-create_time')[0] 
        except:
            return {}
        
        pipeline = collections.OrderedDict()
        
        builds = Build.objects.filter(uuid=latestbuild)
        stage = sorted(list(set([build.task.stage.value for build in builds])))
        
        for key in stage:
            pipeline[key] = {}
            
        for build in builds:
            data = {
                    "buildurl":build.buildurl,
                    "feature":build.feature.name,
                    "status":build.status.name,
                    "task":build.task.name,
                    "params":build.getstaticparams(),
                    "create_time":build.create_time,
                    "lastupdate_time":build.lastupdate_time
                    }
            pipeline[build.task.stage.value][build.name] = data
        return pipeline

class Featurebuilder(models.Model):
    name = models.CharField(max_length=200)
    feature = models.ForeignKey(Feature, on_delete=models.CASCADE)
    uuid = models.CharField(max_length=200,default="")
    create_time = models.DateTimeField(auto_now_add=True)
    lastupdate_time = models.DateTimeField(auto_now=True)

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
    create_time = models.DateTimeField(auto_now_add=True)
    lastupdate_time = models.DateTimeField(auto_now=True)
    
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
        for param in self.feature.params.filter(task=self.task):
            res[param.name] = param.value
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
    create_time = models.DateTimeField(auto_now_add=True)
    lastupdate_time = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name

    





    