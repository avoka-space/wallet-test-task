from django_filters import rest_framework as filters

from apps.wallet.models import Transaction, Wallet


class WalletFilter(filters.FilterSet):
    min_balance = filters.NumberFilter(field_name='balance', lookup_expr='gte')
    max_balance = filters.NumberFilter(field_name='balance', lookup_expr='lte')
    label = filters.CharFilter(field_name='label', lookup_expr='icontains')

    class Meta:
        model = Wallet
        fields = ['min_balance', 'max_balance', 'label']


class TransactionFilter(filters.FilterSet):
    min_amount = filters.NumberFilter(field_name='amount', lookup_expr='gte')
    max_amount = filters.NumberFilter(field_name='amount', lookup_expr='lte')
    txid = filters.CharFilter(field_name='txid', lookup_expr='icontains')
    wallet_id = filters.NumberFilter(field_name='wallet__id')
    created_after = filters.DateTimeFilter(field_name='created_at', lookup_expr='gte')
    created_before = filters.DateTimeFilter(field_name='created_at', lookup_expr='lte')

    class Meta:
        model = Transaction
        fields = ['min_amount', 'max_amount', 'txid', 'wallet_id', 'created_after', 'created_before']
