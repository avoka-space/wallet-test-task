from rest_framework import filters, generics
from apps.wallet.models import Wallet, Transaction
from apps.wallet.serializers import WalletSerializer, TransactionSerializer
from apps.wallet.pagination import WalletPagination, TransactionPagination


class WalletListCreateView(generics.ListCreateAPIView):
    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['label']
    ordering_fields = ['id', 'label', 'balance']
    pagination_class = WalletPagination


class WalletRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer


class TransactionListCreateView(generics.ListCreateAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['wallet__id', 'wallet__label', 'txid', 'created_at']
    ordering_fields = ['id', 'txid', 'amount', 'created_at']
    pagination_class = TransactionPagination


class TransactionRetrieveUpdateDestroyView(generics.RetrieveAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
