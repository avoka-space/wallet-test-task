from rest_framework import filters, generics
from apps.wallet.models import Wallet, Transaction
from apps.wallet.serializers import WalletSerializer, TransactionSerializer
from apps.wallet.pagination import WalletPagination, TransactionPagination
from apps.wallet.filters import WalletFilter, TransactionFilter
from django_filters.rest_framework import DjangoFilterBackend


class WalletListCreateView(generics.ListCreateAPIView):
    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    ordering_fields = ['id', 'label', 'balance']
    pagination_class = WalletPagination
    filterset_class = WalletFilter


class WalletRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer


class TransactionListCreateView(generics.ListCreateAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    ordering_fields = ['txid', 'amount', 'created_at']
    pagination_class = TransactionPagination
    filterset_class = TransactionFilter


class TransactionRetrieveUpdateDestroyView(generics.RetrieveAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
