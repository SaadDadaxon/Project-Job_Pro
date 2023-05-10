from django.shortcuts import render
from rest_framework import generics, permissions
from rest_framework.response import Response
from .serializer import CategorySerializer, StateSerializer, RegionSerializer, CompanyGETSerializer, CompanyPOSTSerializer, TypeSerializer, TagSerializer
from main.models import Category, State, Region, Company, Type, Tag


class CategoryListCreate(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAdminUser]


class StateListCreate(generics.ListCreateAPIView):
    queryset = State.objects.all()
    serializer_class = StateSerializer
    permission_classes = [permissions.IsAdminUser]


class RegionListCreate(generics.ListCreateAPIView):
    queryset = Region.objects.all()
    serializer_class = RegionSerializer
    permission_classes = [permissions.IsAdminUser]

    def get_queryset(self):
        qs = super().get_queryset()
        state_id = self.kwargs.get('state_id')
        qs = qs.filter(state_id=state_id)
        return qs

    def get_serializer_context(self):
        ctx = super().get_serializer_context()
        ctx['state_id'] = self.kwargs.get('state_id')
        return ctx


class RegionRUD(generics.RetrieveUpdateDestroyAPIView):
    queryset = Region.objects.all()
    serializer_class = RegionSerializer
    permission_classes = [permissions.IsAdminUser]


class CompanyListCreate(generics.ListCreateAPIView):
    queryset = Company.objects.all()
    permission_classes = [permissions.IsAdminUser]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CompanyPOSTSerializer
        return CompanyGETSerializer

    # def get_queryset(self):
    #     qs = super().get_queryset()
    #     region_id = self.kwargs['region_id']
    #     qs = qs.filter(region_id=region_id)
    #     return qs
    #
    # def get_serializer_context(self):
    #     ctx = super().get_serializer_context()
    #     ctx['region_id'] = self.kwargs['region_id']
    #     return ctx


class CompanyRUD(generics.RetrieveUpdateDestroyAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanyPOSTSerializer
    permission_classes = [permissions.IsAdminUser]


class TypeListCreate(generics.ListCreateAPIView):
    queryset = Type.objects.all()
    serializer_class = TypeSerializer
    permission_classes = [permissions.IsAdminUser]


class TagListCreate(generics.ListCreateAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [permissions.IsAdminUser]



