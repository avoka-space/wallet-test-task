from decimal import Decimal
from unittest.mock import ANY

from django.forms.models import model_to_dict
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from apps.wallet.models import Transaction, Wallet


class GetTransactionTests(APITestCase):
    def test_get_transaction(self):
        # arrange
        wallet = Wallet.objects.create(label='Test wallet', balance='1.00001')
        transaction = Transaction.objects.create(wallet=wallet, txid='abc', amount='1.00001')

        # act
        response = self.client.get(path=reverse('transaction-detail', args=[transaction.id]), format='json')

        # assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data,
            {'id': transaction.id, 'wallet': wallet.id, 'txid': 'abc', 'amount': '1.00001000', 'created_at': ANY},
        )

    def test_get_transaction__not_found_error(self):
        # act
        response = self.client.get(path=reverse('transaction-detail', args=[1]), format='json')

        # assert
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class CreateTransactionTests(APITestCase):
    def test_create_transaction(self):
        # arrange
        wallet = Wallet.objects.create(label='Test', balance='15')

        # act
        response = self.client.post(
            path=reverse('transaction-list-create'),
            data={'txid': 'cve', 'amount': '-1.3', 'wallet': wallet.id},
            format='json',
        )

        # assert
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Transaction.objects.count(), 1)
        self.assertEqual(Wallet.objects.get().balance, Decimal('13.7'))
        self.assertEqual(
            response.data, {'id': ANY, 'wallet': wallet.id, 'txid': 'cve', 'amount': '-1.30000000', 'created_at': ANY}
        )
        self.assertEqual(
            model_to_dict(Transaction.objects.get()),
            {'id': ANY, 'wallet': wallet.id, 'txid': 'cve', 'amount': Decimal('-1.30000000')},
        )

    def test_create_transaction__negative_balance__bad_request(self):
        # arrange
        wallet = Wallet.objects.create(label='Test', balance='1')

        # act
        response = self.client.post(
            path=reverse('transaction-list-create'),
            data={'txid': 'cve', 'amount': '-1.3', 'wallet': wallet.id},
            format='json',
        )

        # assert
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Transaction.objects.count(), 0)
        self.assertEqual(Wallet.objects.get().balance, Decimal('1'))

    def test_create_transaction__wallet_not_found__bad_request(self):
        # act
        response = self.client.post(
            path=reverse('transaction-list-create'),
            data={'txid': 'cve', 'amount': '1', 'wallet': 1},
            format='json',
        )

        # assert
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Transaction.objects.count(), 0)

    def test_create_transaction__txid_duplicate__bad_request(self):
        # arrange
        wallet = Wallet.objects.create(label='Test', balance='1')
        Transaction.objects.create(wallet=wallet, txid='cve', amount='15')

        # act
        response = self.client.post(
            path=reverse('transaction-list-create'),
            data={'txid': 'cve', 'amount': '33', 'wallet': 1},
            format='json',
        )

        # assert
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Transaction.objects.count(), 1)
        self.assertEqual(Wallet.objects.get().balance, Decimal('16'))

    def test_create_transaction__zero_amount__bad_request(self):
        # arrange
        wallet = Wallet.objects.create(label='Test', balance='1')

        # act
        response = self.client.post(
            path=reverse('transaction-list-create'),
            data={'txid': 'cve', 'amount': '0.00000000', 'wallet': wallet.id},
            format='json',
        )

        # assert
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Transaction.objects.count(), 0)
        self.assertEqual(Wallet.objects.get().balance, Decimal('1'))


class UpdateTransactionTests(APITestCase):
    def test_update_transaction__method_not_implemented(self):
        # arrange
        wallet = Wallet.objects.create(label='Test', balance='1')
        Transaction.objects.create(wallet=wallet, txid='cve', amount='2')

        # act
        response = self.client.put(
            path=reverse('transaction-detail', args=[wallet.id]),
            data={'amount': '-15'},
        )

        # assert
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertEqual(Transaction.objects.get().amount, Decimal('2'))


class DeleteTransactionTests(APITestCase):
    def test_delete_transaction__method_not_implemented(self):
        # arrange
        wallet = Wallet.objects.create(label='Test', balance='1')
        Transaction.objects.create(wallet=wallet, txid='cve', amount='2')

        # act
        response = self.client.delete(
            path=reverse('transaction-detail', args=[wallet.id]),
            data={'amount': '-15'},
        )

        # assert
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertEqual(Transaction.objects.count(), 1)


class GetManyTransactionsTests(APITestCase):
    def test_get_many_transactions(self):
        # arrange
        wallet = Wallet.objects.create(label='Test wallet', balance='100')
        Transaction.objects.create(wallet=wallet, txid='1', amount='2')
        Transaction.objects.create(wallet=wallet, txid='2', amount='2')

        # act
        response = self.client.get(
            path=reverse('transaction-list-create'), data={'ordering': 'created_at'}, format='json'
        )

        # assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data,
            {
                'links': {
                    'first': 'http://testserver/api/v1/transactions/?ordering=created_at&page=1',
                    'last': 'http://testserver/api/v1/transactions/?ordering=created_at&page=1',
                    'next': None,
                    'prev': None,
                },
                'meta': {'pagination': {'count': 2, 'page': 1, 'pages': 1}},
                'results': [
                    {
                        'id': ANY,
                        'txid': '1',
                        'wallet': wallet.id,
                        'amount': '2.00000000',
                        'created_at': ANY,
                    },
                    {
                        'id': ANY,
                        'txid': '2',
                        'wallet': wallet.id,
                        'amount': '2.00000000',
                        'created_at': ANY,
                    },
                ],
            },
        )

    def test_get_many_transactions__pagination(self):
        # arrange
        wallet = Wallet.objects.create(label='Test wallet', balance='100')
        Transaction.objects.create(wallet=wallet, txid='1', amount='2')
        Transaction.objects.create(wallet=wallet, txid='2', amount='3')
        Transaction.objects.create(wallet=wallet, txid='3', amount='4')
        Transaction.objects.create(wallet=wallet, txid='4', amount='5')
        Transaction.objects.create(wallet=wallet, txid='5', amount='6')

        # act
        response = self.client.get(
            path=reverse('transaction-list-create'),
            data={'page': 2, 'page_size': 2, 'ordering': 'created_at'},
            format='json',
        )

        # assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data,
            {
                'links': {
                    'first': 'http://testserver/api/v1/transactions/?ordering=created_at&page=1&page_size=2',
                    'last': 'http://testserver/api/v1/transactions/?ordering=created_at&page=3&page_size=2',
                    'next': 'http://testserver/api/v1/transactions/?ordering=created_at&page=3&page_size=2',
                    'prev': 'http://testserver/api/v1/transactions/?ordering=created_at&page=1&page_size=2',
                },
                'meta': {'pagination': {'count': 5, 'page': 2, 'pages': 3}},
                'results': [
                    {
                        'id': ANY,
                        'txid': '3',
                        'wallet': wallet.id,
                        'amount': '4.00000000',
                        'created_at': ANY,
                    },
                    {
                        'id': ANY,
                        'txid': '4',
                        'wallet': wallet.id,
                        'amount': '5.00000000',
                        'created_at': ANY,
                    },
                ],
            },
        )

    def test_get_many_transactions__searching_by_wallet_id(self):
        # arrange
        wallet1 = Wallet.objects.create(label='Test 1', balance='1')
        wallet2 = Wallet.objects.create(label='Test 2', balance='1')
        Transaction.objects.create(wallet=wallet1, txid='1', amount='2')
        Transaction.objects.create(wallet=wallet2, txid='2', amount='3')

        # act
        response = self.client.get(
            path=reverse('transaction-list-create'),
            data={'wallet_id': wallet1.id, 'ordering': 'created_at'},
            format='json',
        )

        # assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data,
            {
                'links': {
                    'first': f'http://testserver/api/v1/transactions/?ordering=created_at&page=1&wallet_id={wallet1.id}',
                    'last': f'http://testserver/api/v1/transactions/?ordering=created_at&page=1&wallet_id={wallet1.id}',
                    'next': None,
                    'prev': None,
                },
                'meta': {'pagination': {'count': 1, 'page': 1, 'pages': 1}},
                'results': [
                    {
                        'id': ANY,
                        'txid': '1',
                        'wallet': wallet1.id,
                        'amount': '2.00000000',
                        'created_at': ANY,
                    },
                ],
            },
        )

    def test_get_many_transactions__searching_by_txid(self):
        # arrange
        wallet = Wallet.objects.create(label='Test 1', balance='1')
        Transaction.objects.create(wallet=wallet, txid='a pattern f', amount='2')
        Transaction.objects.create(wallet=wallet, txid='wel', amount='3')
        Transaction.objects.create(wallet=wallet, txid='bfb pattern cdkk', amount='3')

        # act
        response = self.client.get(
            path=reverse('transaction-list-create'), data={'txid': 'pattern', 'ordering': 'created_at'}, format='json'
        )

        # assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data,
            {
                'links': {
                    'first': 'http://testserver/api/v1/transactions/?ordering=created_at&page=1&txid=pattern',
                    'last': 'http://testserver/api/v1/transactions/?ordering=created_at&page=1&txid=pattern',
                    'next': None,
                    'prev': None,
                },
                'meta': {'pagination': {'count': 2, 'page': 1, 'pages': 1}},
                'results': [
                    {
                        'id': ANY,
                        'txid': 'a pattern f',
                        'wallet': wallet.id,
                        'amount': '2.00000000',
                        'created_at': ANY,
                    },
                    {
                        'id': ANY,
                        'txid': 'bfb pattern cdkk',
                        'wallet': wallet.id,
                        'amount': '3.00000000',
                        'created_at': ANY,
                    },
                ],
            },
        )

    def test_get_many_transactions__filtering_by_amount(self):
        # arrange
        wallet = Wallet.objects.create(label='Test 1', balance='500')
        Transaction.objects.create(wallet=wallet, txid='a', amount='100')
        Transaction.objects.create(wallet=wallet, txid='b', amount='-50')
        Transaction.objects.create(wallet=wallet, txid='c', amount='-120')
        Transaction.objects.create(wallet=wallet, txid='d', amount='300')

        # act
        response = self.client.get(
            path=reverse('transaction-list-create'),
            data={'min_amount': '-100', 'max_amount': '105', 'ordering': '-amount'},
            format='json',
        )

        # assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data,
            {
                'links': {
                    'first': 'http://testserver/api/v1/transactions/?max_amount=105&min_amount=-100&ordering=-amount&page=1',
                    'last': 'http://testserver/api/v1/transactions/?max_amount=105&min_amount=-100&ordering=-amount&page=1',
                    'next': None,
                    'prev': None,
                },
                'meta': {'pagination': {'count': 2, 'page': 1, 'pages': 1}},
                'results': [
                    {
                        'id': ANY,
                        'txid': 'a',
                        'wallet': wallet.id,
                        'amount': '100.00000000',
                        'created_at': ANY,
                    },
                    {
                        'id': ANY,
                        'txid': 'b',
                        'wallet': wallet.id,
                        'amount': '-50.00000000',
                        'created_at': ANY,
                    },
                ],
            },
        )
