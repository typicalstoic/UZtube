from django.urls import path
from .views import *


urlpatterns = [
    path('api/v1/categories/', category_list_view),
    path('api/v1/contents/', content_list_view),
    path('api/v1/contents/<int:pk>', content_by_category),
    path('api/v1/content/<int:pk>', content_detail),
    path('api/v1/create/', comment_create),
]




