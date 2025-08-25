from django.urls import path
from .views import *

urlpatterns = [
    # path('', index_view, name='main'),
    # path('category/<int:category_id>', get_category_content, name='category'),
    # path('content/<int:pk>', video_content_detail, name='content'),
    # path('add_content/', add_new_content, name='add_content')


    path('', ContentListView.as_view(), name='main'),
    path('category/<int:category_id>', ContentByCategory.as_view(), name='category'),
    path('content/<int:pk>', VideoContentDetail.as_view(), name='content'),
    path('add_content/', NewContent.as_view(), name='add_content'),
    path('login/', user_login_vew, name='login'),
    path('logout/', user_logout_view, name='logout'),
    path('registration/', register_user_view, name='register'),
    path('save/comment/<int:pk>/', comment_save_view, name='comment_save'),
    path('comment/delete/<int:pk>/', comment_delete, name='comment_delete'),
    path('search/', SearchContent.as_view(), name='search'),
    path('profile/<int:pk>/', profile_view, name='profile'),
    path('edit/profile/', edit_profile_view, name='edit_profile'),
    path('edit/account/', edit_account_view, name='edit_account'),
    path('content/update/<int:pk>/', UpdateContentview.as_view(), name='update_content'),
    path('content/delete/<int:pk>/', DeleteContentView.as_view(), name='delete_content'),
    path('comment/update/<int:pk>/', UpdateCommentView.as_view(), name='comment_update'),


]