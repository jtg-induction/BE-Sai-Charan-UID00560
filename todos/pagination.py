from rest_framework.pagination import PageNumberPagination


class StandardResultsSetPagination(PageNumberPagination):
    """
    Class for handling pagination of todo objects.
    """

    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100
