# courses/pagination.py
from rest_framework.pagination import PageNumberPagination

class CoursePagination(PageNumberPagination):
    page_size = 6
    page_size_query_param = 'page_size'  # позволит фронту менять размер: ?page_size=12
    max_page_size = 50  # максимум 50 курсов за раз


class CategoryPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class AssignmentPagination(PageNumberPagination):
    page_size = 15
    page_size_query_param = 'page_size'
    max_page_size = 75

class SubmissionPagination(PageNumberPagination):
    page_size = 12
    page_size_query_param = 'page_size'
    max_page_size = 100

class GradePagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100