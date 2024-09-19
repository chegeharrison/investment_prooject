from rest_framework import serializers
from .models import InvestmentAccount, Transaction, AccountMembership
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class InvestmentAccountSerializer(serializers.ModelSerializer):
    users = UserSerializer(many=True, read_only=True)
    
    class Meta:
        model = InvestmentAccount
        fields = ['id', 'name', 'description', 'users']

class AccountMembershipSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    account = InvestmentAccountSerializer()
    
    class Meta:
        model = AccountMembership
        fields = ['user', 'account', 'permission']

class TransactionSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    account = InvestmentAccountSerializer()
    
    class Meta:
        model = Transaction
        fields = ['id', 'account', 'user', 'amount', 'date', 'description']
