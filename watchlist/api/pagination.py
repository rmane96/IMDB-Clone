from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination

class WatchListPagination(LimitOffsetPagination):
    page_size = 5

    