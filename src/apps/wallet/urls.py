from django.urls import path
from apps.wallet import views


urlpatterns = [
    path('wallets/', views.WalletListCreateView.as_view(), name='wallet-list-create'),
    path('wallets/<int:pk>/', views.WalletRetrieveUpdateDestroyView.as_view(), name='wallet-detail'),
    path('transactions/', views.TransactionListCreateView.as_view(), name='transaction-list-create'),
    path('transactions/<int:pk>/', views.TransactionRetrieveUpdateDestroyView.as_view(), name='transaction-detail'),
]
