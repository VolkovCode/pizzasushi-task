from django.contrib import admin

from .models import Account, Replenishment, Debiting, Transfer

EMPTY_VALUE = '-пусто-'

@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'balance')
    search_fields = ('id',)
    list_filter = ('id', 'user', 'balance')
    empty_value_display = EMPTY_VALUE


@admin.register(Replenishment)
class ReplenishmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'amount', 'date', 'account')
    search_fields = ('account',)
    list_filter = ('date', 'account')
    empty_value_display = EMPTY_VALUE


@admin.register(Debiting)
class DebitingAdmin(admin.ModelAdmin):
    list_display = ('id', 'amount', 'date', 'account')
    search_fields = ('account',)
    list_filter = ('date', 'account')
    empty_value_display = EMPTY_VALUE


@admin.register(Transfer)
class TransferAdmin(admin.ModelAdmin):
    list_display = ('id', 'from_account', 'to_account', 'amount', 'date')
    search_fields = ('from_account', 'to_account')
    list_filter = ('date', 'from_account', 'to_account')
    empty_value_display = EMPTY_VALUE
