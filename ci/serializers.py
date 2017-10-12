# -*- coding: utf-8 -*-
from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import *
from rest_framework.exceptions import ErrorDetail, ValidationError
import time,json,uuid
from .utils import task_client

class JSONSerializerField(serializers.Field):
    """ Serializer for JSONField -- required to make field writable"""

    def to_internal_value(self, data):
        json_data = {}
        try:
            json_data = json.loads(data)
        except ValueError, e:
            pass
        finally:
            return json_data
    
    def to_representation(self, value):
        return value

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"

class TaskSerializer(serializers.ModelSerializer):
    product = serializers.CharField(source="product.name",read_only=True)
    type = serializers.CharField(source="type.name",read_only=True)
    stage = serializers.CharField(source="stage.name",read_only=True)
    params = JSONSerializerField(source="getcustomparams",)
    class Meta:
        model = Task
        fields = ('id','name', 'product', 'type','stage','params')

class ModuleSerializer(serializers.ModelSerializer):
    type = serializers.CharField(source="type.name",read_only=True)
    product = serializers.CharField(source="product.name",read_only=True)
    repositoryserver = serializers.CharField(source="repositoryserver.server",read_only=True)
    class Meta:
        model = Module
        fields = ('id','name','repository','repositoryserver', 'type','product',)

class BuildSerializer(serializers.ModelSerializer):
    params = JSONSerializerField(source="getstaticparams",)
    taskname = serializers.CharField(source="task.name",read_only=True)
    stage = serializers.CharField(source="task.stage.name",read_only=True)
    status = serializers.CharField(source="status.name",read_only=True)
    trigger = serializers.CharField(source="trigger.name",read_only=True)
    gearman = serializers.CharField(source="distributor.name",read_only=True)
    
    class Meta:
        model = Build
        fields = ["taskname","stage","status","params","trigger","gearman","buildurl"]
        
class FeaturebuilderSerializer(serializers.ModelSerializer):
#     builds = BuildSerializer(read_only=True, many=True)
    feature = serializers.CharField(source="feature.name",read_only=True)
    featureid = serializers.CharField(source="feature.featureid")
    builds = BuildSerializer(source='getbuilddetail', many=True)
    class Meta:
        model = Featurebuilder
        fields = ["feature","uuid","featureid",'builds']
        read_only_fields = ["uuid"]
    
    def validate(self, attrs):
        requestData = self._kwargs['data']
        validatedData = {}
        try:
            feature = Feature.objects.get(featureid=requestData.get("featureid"))
            validatedData["feature"] = feature
            validatedData["name"] = "{}_{}".format(feature.product.name,feature.name)
            validatedData["uuid"] = uuid.uuid1().hex
        except:
            raise serializers.ValidationError("feature does not exist,please check your feature name")
        
        return validatedData
    
    def create(self, validated_data):
        tasks = validated_data.get("feature").task.all()
        pipeline = validated_data.get("feature").getpipeline()
        fb = Featurebuilder.objects.create(**validated_data)
        
        for stage,tasks in pipeline.items():
            for key,value in pipeline[stage].items():
                data = {}
                data["task"] = value
                data["name"] = "{}:{}:{}".format(fb.uuid,fb.feature.name,value.name)
                data["uuid"] = fb
                data["distributor"] = value.gearman
                data["feature"] = fb.feature
                data["status"],_ = Status.objects.get_or_create(name="created")
                data["trigger"] = User.objects.get(username=self.context["request"].user)
                instance,_ = Build.objects.get_or_create(**data)
                instance.params = json.dumps(instance.getdynamicparams())
                # 分发任务到gearman,并更新状态
                if stage == pipeline.keys()[0]:
                    instance.status,_ = Status.objects.get_or_create(name="waiting")
                    t = task_client(instance)
                    t.trigger_builder()
                    
                instance.save()
        return fb

#######done

class ParamSerializer(serializers.ModelSerializer):
    task = serializers.CharField(source="task.name",read_only=True)
    table = serializers.CharField(source="getboundtable",read_only=True)
    class Meta:
        model = Param
        fields = ('name', 'value', 'task','table')


class FeatureSerializer(serializers.ModelSerializer):
    product = serializers.CharField(source="product.name",)
    type = serializers.CharField(source="type.name",)
    task = TaskSerializer(read_only=True, many=True)
    module = ModuleSerializer(read_only=True, many=True)
    params = JSONSerializerField(source="getcurrent_vars",read_only=True)
#     testbuilds = BuildSerializer(source='getlatestbuild', many=True)
    
    class Meta:
        model = Feature
#         fields = ('name', 'product', 'type','task','module','testbuilds','params')
        fields = ('id','branch','featureid','name', 'product', 'type','task','module','params')

    def validate(self, attrs):
        pass
    def update(self, instance, validated_data):
        pass   

###########done
class PipeLineSerializer(serializers.ModelSerializer):
    pipeline = JSONSerializerField(source="getlatestpipeline",read_only=True)
    class Meta:
        model = Feature
        fields = ('pipeline',)
        
class NewfeatureSerializer(serializers.ModelSerializer):
    product = serializers.CharField(source="product.name",read_only=True)
    type = serializers.CharField(source="type.name",read_only=True)
    task = TaskSerializer(read_only=True, many=True)
    module = ModuleSerializer(read_only=True, many=True)
    
#     testbuilds = BuildSerializer(source='getlatestbuild', many=True)
    
    class Meta:
        model = Feature
#         fields = ('name', 'product', 'type','task','module','testbuilds')
        fields = ('name', 'product', 'type','task','module')
        

#############done
class UpstatusSerializer(serializers.ModelSerializer):
    
    feature = serializers.CharField(source="feature.name",read_only=True)
    featureid = serializers.CharField(source="feature.featureid",read_only=True)
    
#     params = serializers.JSONField(source="getstaticparams",read_only=True)
    params = JSONSerializerField(source="getstaticparams",read_only=True)
    
    taskname = serializers.CharField(source="task.name",read_only=True)
    stage = serializers.CharField(source="task.stage.name",read_only=True)
    status = serializers.CharField(source="status.name",)
    trigger = serializers.CharField(source="trigger.name",read_only=True)
    gearman = serializers.CharField(source="distributor.name",read_only=True)
    
    class Meta:
        model = Build
        fields = ["name","taskname","stage","status","params","trigger","gearman","buildurl","featureid","feature",]
        read_only_fields = ('distributor','task','trigger','params','feature')
    
    def validate(self, attrs):
        requestData = self._kwargs['data']
        validatedData = {}
        validatedData["name"] = requestData.get("name")
        
        status = Status.objects.filter(name=requestData.get("status"))
        if not status:
            raise serializers.ValidationError("build status error,please post correct status value!")
        
        validatedData["status"] = status[0]
        validatedData["buildurl"] = requestData.get("buildurl")
        return validatedData
        
    def update(self, instance, validated_data):
        
        if instance.name == validated_data.get("name"):
            instance.status = validated_data.get("status")
            instance.buildurl = validated_data.get("buildurl") 
            instance.save()
             #check current stage tasks finished or not
            pipeline = instance.feature.getpipeline(instance.uuid)
            pipekeys = pipeline.keys()
            c_stage = instance.task.stage.value
            idx = pipekeys.index(c_stage)
            is_finished = True
            
            for build in pipeline[c_stage].values():
                if build.status.name != "passed" and build.parent is None:
                    is_finished = False 
                    
            #send next stage build
            if idx == len(pipekeys)-1 or not is_finished:
                pass
            else :
                for build in pipeline[pipekeys[idx+1]].values():
                    t = task_client(build)
                    t.trigger_builder() 
            
            return instance
        else:
            name = "sub_{}_{}".format(instance.name,validated_data.get("name"))
            new_instance,created = Build.objects.get_or_create(parent=instance,name=name)
            if created:
                new_instance.trigger = instance.trigger
                new_instance.feature = instance.feature
                new_instance.distributor = instance.distributor
                new_instance.task = instance.task
                new_instance.uuid = instance.uuid
                new_instance.parent = instance
                
            new_instance.status = validated_data.get("status")
            new_instance.buildurl = validated_data.get("buildurl")
            new_instance.save()
       
        return new_instance
    
    
    