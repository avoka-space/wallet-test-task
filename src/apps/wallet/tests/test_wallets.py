from unittest.mock import ANY
from decimal import Decimal

from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from django.forms.models import model_to_dict

from apps.wallet.models import Wallet


class GetWalletTests(APITestCase):
    def test_get_wallet(self):
        # arrange
        wallet = Wallet.objects.create(label='Test wallet', balance='1.00001')

        # act
        response = self.client.get(path=reverse('wallet-detail', args=[wallet.id]), format='json')

        # assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'id': wallet.id, 'label': 'Test wallet', 'balance': '1.00001000'})

    def test_get_wallet__not_found_error(self):
        # act
        response = self.client.get(path=reverse('wallet-detail', args=[11]), format='json')

        # assert
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class CreateWalletTests(APITestCase):
    def test_create_wallet(self):
        # act
        response = self.client.post(
            path=reverse('wallet-list-create'),
            data={'label': 'Test wallet', 'balance': '100'},
            format='json',
        )

        # assert
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Wallet.objects.count(), 1)
        self.assertEqual(model_to_dict(Wallet.objects.get()), {'id': ANY, 'label': 'Test wallet', 'balance': Decimal('0')})
        self.assertEqual(response.data, {'id': ANY, 'label': 'Test wallet', 'balance': '0.00000000'})


class UpdateWalletTests(APITestCase):
    def test_update_wallet(self):
        # arrange
        wallet = Wallet.objects.create(label='Test wallet', balance='1.00001')

        # act
        response = self.client.put(
            path=reverse('wallet-detail', args=[wallet.id]),
            data={'label': 'New name', 'balance': '100'},
            format='json',
        )

        # assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(model_to_dict(Wallet.objects.get(id=wallet.id)), {'id': wallet.id, 'label': 'New name', 'balance': Decimal('1.00001')})
        self.assertEqual(response.data, {'id': ANY, 'label': 'New name', 'balance': '1.00001000'})

    def test_update_wallet__not_found_error(self):
        # act
        response = self.client.get(path=reverse('wallet-detail', args=[11]), format='json')

        # assert
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class DeleteWalletTests(APITestCase):
    def test_delete_wallet(self):
        # arrange
        wallet = Wallet.objects.create(label='Test wallet', balance='1.00001')

        # act
        response = self.client.delete(
            path=reverse('wallet-detail', args=[wallet.id])
        )

        # assert
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Wallet.objects.count(), 0)

    def test_update_wallet__not_found_error(self):
        # act
        response = self.client.delete(path=reverse('wallet-detail', args=[11]))

        # assert
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class GetManyWalletsTests(APITestCase):
    def test_get_many_wallets(self):
        # arrange
        Wallet.objects.create(label='Test wallet', balance='1')
        Wallet.objects.create(label='Second wallet', balance='1')

        # act
        response = self.client.get(path=reverse('wallet-list-create'), data={'ordering': 'id'}, format='json')

        # assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data,
            {
                "count": 2,
                "next": None,
                "previous": None,
                "results": [
                    {
                        "id": ANY,
                        "label": "Test wallet",
                        "balance": "1.00000000"
                    },
                    {
                        "id": ANY,
                        "label": "Second wallet",
                        "balance": "1.00000000"
                    },
                ]
            }
        )

    def test_get_many_wallets__pagination(self):
        # arrange
        Wallet.objects.create(label='AAA', balance='1')
        Wallet.objects.create(label='BBB', balance='1')
        Wallet.objects.create(label='CCC', balance='1')
        Wallet.objects.create(label='DDD', balance='1')
        Wallet.objects.create(label='EEE', balance='1')

        # act
        response = self.client.get(
            path=reverse('wallet-list-create'),
            data={'page': 2, 'page_size': 2, 'ordering': 'label'},
            format='json')

        # assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data,
            {
                "count": 5,
                "next": 'http://testserver/api/v1/wallets/?ordering=label&page=3&page_size=2',
                "previous": 'http://testserver/api/v1/wallets/?ordering=label&page_size=2',
                "results": [
                    {
                        "id": ANY,
                        "label": "CCC",
                        "balance": "1.00000000"
                    },
                    {
                        "id": ANY,
                        "label": "DDD",
                        "balance": "1.00000000"
                    },
                ]
            }
        )

    def test_get_many_wallets__not_valid_page__not_found_error(self):
        # arrange
        Wallet.objects.create(label='AAA', balance='1')
        Wallet.objects.create(label='BBB', balance='1')

        # act
        response = self.client.get(
            path=reverse('wallet-list-create'),
            data={'page': 2, 'page_size': 2},
            format='json')

        # assert
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_many_wallets__searching(self):
        # arrange
        Wallet.objects.create(label='Jason Wallet', balance='1')
        Wallet.objects.create(label='my new walleT', balance='1')
        Wallet.objects.create(label='Testing', balance='1')
        Wallet.objects.create(label='White wall', balance='1')

        # act
        response = self.client.get(
            path=reverse('wallet-list-create'),
            data={'label': 'wallet', 'ordering': 'id'},
            format='json')

        # assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data,
            {
                "count": 2,
                "next": None,
                "previous": None,
                "results": [
                    {
                        "id": ANY,
                        "label": "Jason Wallet",
                        "balance": "1.00000000"
                    },
                    {
                        "id": ANY,
                        "label": "my new walleT",
                        "balance": "1.00000000"
                    },
                ]
            }
        )

    def test_get_many_wallets__balance_filtering(self):
        # arrange
        Wallet.objects.create(label='A', balance='150')
        Wallet.objects.create(label='B', balance='11')
        Wallet.objects.create(label='C', balance='1')
        Wallet.objects.create(label='D', balance='600')

        # act
        response = self.client.get(
            path=reverse('wallet-list-create'),
            data={'min_balance': '10.9', 'max_balance': '150.0', 'ordering': 'label'},
            format='json')

        # assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data,
            {
                "count": 2,
                "next": None,
                "previous": None,
                "results": [
                    {
                        "id": ANY,
                        "label": "A",
                        "balance": "150.00000000"
                    },
                    {
                        "id": ANY,
                        "label": "B",
                        "balance": "11.00000000"
                    },
                ]
            }
        )
