from django.shortcuts import render
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from .models import InvestmentAccount, Transaction, AccountMembership
from .serializers import InvestmentAccountSerializer, TransactionSerializer
from .permissions import CanViewAccount, CanManageAccount, CanPostTransaction, IsAccountOwner


# Create your views here.
class InvestmentAccountViewSet(viewsets.ModelViewSet):
    queryset = InvestmentAccount.objects.all()
    serializer_class = InvestmentAccountSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.IsAuthenticated(), CanViewAccount()]
        elif self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAuthenticated(), CanManageAccount()]
        return [permissions.IsAuthenticated()]

class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

    def get_permissions(self):
        if self.action == 'create':
            return [permissions.IsAuthenticated(), CanPostTransaction()]
        elif self.action in ['list', 'retrieve']:
            return [permissions.IsAuthenticated(), IsAccountOwner()]
        return [permissions.IsAuthenticated()]
    
    def perform_create(self, serializer):
        account = serializer.validated_data['account']
        if not account.accountmembership_set.filter(user=self.request.user, permission='post').exists():
            raise permissions.PermissionDenied('You do not have permission to post transactions to this account.')
        serializer.save(user=self.request.user)
