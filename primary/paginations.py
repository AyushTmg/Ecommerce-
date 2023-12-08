from rest_framework.pagination import PageNumberPagination

class Default(PageNumberPagination):
    page_size = 10
