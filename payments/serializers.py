from rest_framework import serializers

from .models import Account, Replenishment, Debiting, Transfer


class AccountSerializer(serializers.ModelSerializer): 
    
    class Meta:
        model = Account
        fields = ['id', 'user_id', 'balance']
        read_only_fields = ('id', 'user_id', 'balance')


class ReplenishmentSerializer(serializers.ModelSerializer):
    id = serializers.CharField(source='account.user')

    class Meta:
        model = Replenishment
        fields = ('id', 'amount', 'date')
        read_only_fields = ('date',)

    def create(self, validated_data):
        validated_data['account'].balance += validated_data['amount']
        validated_data['account'].save()
        return super().create(validated_data)
    

class DebitingSerializer(serializers.ModelSerializer):
    id = serializers.CharField(source='account.user')

    class Meta:
        model = Debiting
        fields = ('id', 'amount', 'date')
        read_only_fields = ('date',)

    def create(self, validated_data):
        balance = validated_data['account'].balance
        amount = validated_data['amount']
        if amount < 0 or amount > balance:
            raise serializers.ValidationError('Недостаточно средств!')
        validated_data['account'].balance -= validated_data['amount']
        validated_data['account'].save()
        return super().create(validated_data)
    

class TransferSerializer(serializers.ModelSerializer):
    from_user_id = serializers.CharField(source='from_accountt.user', label='id пользователя-отправителя')
    to_user_id = serializers.CharField(source='to_account.user', label='id пользователя-получателя')

    class Meta:
        model = Transfer
        fields = ('from_user_id', 'to_user_id', 'amount', 'date')
