from django.db import models
from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser, Group, Permission

# Create your models here.
class User(AbstractUser):
    groups = models.ManyToManyField(
        Group,
        related_name='custom_user_set',  # Changed related_name
        blank=True,
        help_text='The groups this user belongs to.',
        related_query_name='custom_user'
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='custom_user_set',  # Changed related_name
        blank=True,
        help_text='Specific permissions for this user.',
        related_query_name='custom_user'
    )

class InvestmentAccount(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    users = models.ManyToManyField(User, through='AccountMembership')

    def __str__(self):
        return self.name

class AccountMembership(models.Model):
    ACCOUNT_PERMISSIONS = (
        ('view', 'View Only'),
        ('full', 'Full CRUD'),
        ('post', 'Post Transactions'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    account = models.ForeignKey(InvestmentAccount, on_delete=models.CASCADE)
    permission = models.CharField(max_length=10, choices=ACCOUNT_PERMISSIONS)

    class Meta:
        unique_together = ('user', 'account')

    def __str__(self):
        return f'{self.user.username} - {self.account.name} - {self.permission}'

class Transaction(models.Model):
    account = models.ForeignKey(InvestmentAccount, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'{self.user.username} - {self.amount} - {self.date}'

