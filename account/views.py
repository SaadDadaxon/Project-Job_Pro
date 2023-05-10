from django.shortcuts import render
from rest_framework import generics, status, permissions
from account.permission import IsOwnUserOrReadOnly
from rest_framework.response import Response

from .models import Account, WorkingHistory
from .serializer import RegisterSerializer, LoginSerializer, MyAccountSerializer, AccountUpdateSerializer, \
    WorkingHistoryGETSerializer, WorkingHistoryPOSTSerializer


class AccountRegister(generics.GenericAPIView):
    # http://127.0.0.1:8000/account/api/register/
    serializer_class = RegisterSerializer

    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'success': True, 'message': 'Hisob muofaqiyatli yaratildi'})


class AccountLogin(generics.GenericAPIView):
    # http://127.0.0.1:8000/account/api/login/
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'success': True, 'data': serializer.data['tokens']}, status=status.HTTP_200_OK)


class MyAccount(generics.GenericAPIView):
    # http://127.0.0.1:8000/account/api/my-account/
    serializer_class = MyAccountSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        serializer = self.serializer_class(user)
        return Response({'success': True, 'data': serializer.data}, status=status.HTTP_200_OK)


class AccountRU(generics.RetrieveUpdateAPIView):
    # http://127.0.0.1:8000/account/api/retrive-update/<int:id>/
    serializer_class = AccountUpdateSerializer
    queryset = Account.objects.all()
    permission_classes = [permissions.IsAuthenticated, IsOwnUserOrReadOnly]

    def get(self, request, *args, **kwargs):
        query = self.get_object()
        if query:
            serializer = self.serializer_class(query)
            return Response({'success': True, 'data': serializer.data}, status=status.HTTP_200_OK)
        return Response({'success': False, 'message': "so'rov mavjud emas edi"})

    def put(self, request, *args, **kwargs):
        obj = self.get_object()
        serializer = self.serializer_class(obj, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({'success': True, 'data': serializer.data}, status=status.HTTP_200_OK)
        return Response({'success': False, 'message': 'hisob ma’lumotlari yaroqsiz'})


class WorkingHistoryList(generics.ListCreateAPIView):
    queryset = WorkingHistory.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return WorkingHistoryPOSTSerializer
        return WorkingHistoryGETSerializer






    





