from django.contrib import admin
from .models import User, InvestmentAccount, AccountMembership, Transaction

# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    pass

@admin.register(InvestmentAccount)
class InvestmentAccountAdmin(admin.ModelAdmin):
    pass

@admin.register(AccountMembership)
class AccountMembershipAdmin(admin.ModelAdmin):
    pass

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('account', 'user', 'amount', 'date', 'description')
    list_filter = ('date', 'account')
    search_fields = ('user__username', 'description')
