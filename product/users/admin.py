from django.contrib import admin
from django import forms

from users.models import Balance


class AddBalanceAdminForm(forms.ModelForm):

    amount = forms.IntegerField(label='Amount')

    class Meta:
        model = Balance
        fields = ('user',)


@admin.register(Balance)
class BalanceAdmin(admin.ModelAdmin):

    form = AddBalanceAdminForm

    def save_model(self, request, obj, form, change):
        form = AddBalanceAdminForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            user_id = form.cleaned_data['user']
            user_balance = Balance.objects.get(user=user_id)
            user_balance.bonus += amount

            super().save_model(request, user_balance, form, change)