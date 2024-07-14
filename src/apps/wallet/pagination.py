from rest_framework_json_api.pagination import JsonApiPageNumberPagination


class WalletPagination(JsonApiPageNumberPagination):
    page_query_param = 'page'
    page_size_query_param = 'page_size'
    max_page_size = 100


class TransactionPagination(JsonApiPageNumberPagination):
    page_query_param = 'page'
    page_size_query_param = 'page_size'
    max_page_size = 1000
