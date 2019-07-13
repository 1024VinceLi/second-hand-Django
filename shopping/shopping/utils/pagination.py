from rest_framework.pagination import PageNumberPagination

"""
分页配置
"""
class StandardResultPagination(PageNumberPagination):
    page_size = 2
    page_size_query_param = 'page_size'
    max_page_size = 20