from typing import Any

from rest_framework import serializers

from apps.wallet.models import Transaction, Wallet


class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = '__all__'
        read_only_fields = ['balance']

    def create(self, validated_data: dict[str, Any]) -> Wallet:
        validated_data['balance'] = 0
        return super().create(validated_data)


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'

    def create(self, validated_data: dict[str, Any]) -> Transaction:
        if validated_data['amount'] == 0:
            raise serializers.ValidationError('Amount cannot be negative')
        return super().create(validated_data)
