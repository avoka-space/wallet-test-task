from django.urls import path
from apps.wallet import views


urlpatterns = [
    path('v1/wallets/', views.WalletListCreateView.as_view(), name='wallet-list-create'),
    path('v1/wallets/<int:pk>/', views.WalletRetrieveUpdateDestroyView.as_view(), name='wallet-detail'),
    path('v1/transactions/', views.TransactionListCreateView.as_view(), name='transaction-list-create'),
    path('v1/transactions/<int:pk>/', views.TransactionRetrieveUpdateDestroyView.as_view(), name='transaction-detail'),
]
