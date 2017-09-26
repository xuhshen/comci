# -*- coding: utf-8 -*-
from django.shortcuts import render

from django.http import HttpResponse,Http404
from django.contrib.auth.models import User
from rest_framework import viewsets
from .models import *
from .serializers import FeatureSerializer,BuildSerializer,FeaturebuilderSerializer,UpstatusSerializer

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from rest_framework import mixins
from rest_framework import generics
from rest_framework.exceptions import ErrorDetail, ValidationError
from rest_framework import permissions
from .utils import task_client

# Create your views here.

class FeatureViewSet(mixins.ListModelMixin,
                  generics.GenericAPIView):
    """
    API endpoint that allows users to be viewed or edited.
    """
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = FeatureSerializer
    
    def get_queryset(self):
        queryset = Feature.objects.filter()
        return queryset
    
    def get(self, request, *args, **kwargs): 
        return self.list(self, request, *args, **kwargs)
 

class TriggerViewSet(mixins.ListModelMixin,
                    mixins.CreateModelMixin,
                  generics.GenericAPIView):

    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = FeaturebuilderSerializer
    
    def get_queryset(self):
        queryset = Featurebuilder.objects.filter()
        return queryset

    def post(self, request, *args, **kwargs):
        '''
        '''
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)



class UpstatusViewSet(mixins.ListModelMixin,
                      mixins.UpdateModelMixin,
                  generics.GenericAPIView):
    
    '''更新build 状态，
    '''

    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = UpstatusSerializer
    
    def get_queryset(self):
        queryset = Build.objects.filter()
        return queryset
    
    def get(self, request, *args, **kwargs): 
        return self.list(self, request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}
        
        return Response(serializer.data) 
     
     
        