from django.shortcuts import render
from rest_framework import mixins, status, viewsets
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .models import Account, Transfer, User, Replenishment, Debiting
import decimal
from .serializers import (
    AccountSerializer, 
    ReplenishmentSerializer, 
    DebitingSerializer, 
    TransferSerializer
)


class BalanceViewSet(mixins.ListModelMixin,
                     mixins.RetrieveModelMixin,
                     viewsets.GenericViewSet):
    serializer_class = AccountSerializer
    queryset = Account.objects.all()

    def retrieve(self, request, *args, **kwargs):
        user_id = self.kwargs.get('pk')
        user = User.objects.get(id=user_id)
        queryset = Account.objects.get(user=user)
        serializer = self.get_serializer(queryset)
        return Response(serializer.data)
        

class ReplenishmentViewSet(mixins.CreateModelMixin,
                           viewsets.GenericViewSet):
    serializer_class = ReplenishmentSerializer
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user_id = self.request.data.get('id')
        
        try:
            user = User.objects.get(id=user_id)
        except Exception:
            return Response(
                {'id': 'Укажите id существующего пользователя!'},
                status=status.HTTP_400_BAD_REQUEST
            )
        try:
            account = Account.objects.get(user = user)
        except Exception:
            Account.objects.create(user=user)
            account = Account.objects.get(user = user)
        serializer.save(account=account)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )
    

class DebitingViewSet(mixins.CreateModelMixin,
                      viewsets.GenericViewSet):
    queryset = Debiting.objects.all()
    serializer_class = DebitingSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user_id = self.request.data.get('id')
        
        try:
            user = User.objects.get(id=user_id)
        except Exception:
            return Response(
                {'id': 'Укажите id существующего пользователя!'},
                status=status.HTTP_400_BAD_REQUEST
            )
        try:
            account = Account.objects.get(user = user)
        except Exception:
            Account.objects.create(user=user)
            account = Account.objects.get(user = user)
        serializer.save(account=account)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )
    

class TransferViewSet(viewsets.GenericViewSet,
                      mixins.CreateModelMixin):
    serializer_class = TransferSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            from_account = Account.objects.get(
            user=self.request.data['from_user_id']
        )
        except Exception:
            return Response(
                {'id': 'Укажите id существующего пользователя!'},
                status=status.HTTP_400_BAD_REQUEST
            )
        try:
            to_account = Account.objects.get(
            user=self.request.data['to_user_id']
        )
        except Exception:
            return Response(
                {'id': 'Укажите id существующего пользователя!'},
                status=status.HTTP_400_BAD_REQUEST
            )
        amount = self.request.data['amount']
        
        if from_account == to_account:
            return Response(
                {'error': 'Получатель и отправитель совпадают!'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            if from_account.balance < 0 or from_account.balance < decimal.Decimal(amount):
                raise ValueError
            
            from_account.balance -= decimal.Decimal(amount)
            from_account.save() 
            to_account.balance += decimal.Decimal(amount)
            to_account.save()

            Transfer.objects.create(
                from_account=from_account,
                to_account=to_account,
                amount=amount
            )
        except ValueError:
            return Response(
                {'amount': 'Недостаточно средств '
                           'для перевода!'},
                status=status.HTTP_402_PAYMENT_REQUIRED
            )

        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )
    