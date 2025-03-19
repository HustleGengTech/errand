from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views
urlpatterns = [
    path('home', views.Home, name='home' ),
    path('profile/', views.ProfileView, name='profile' ),
    path('dashboard/<str:username>/', views.DashboardView, name='dashboard' ),
    path('dashboard/<str:username>/', views.DashboardView, name='user_dashboard'),  # Another user's
    path('edit-profile/', views.EditProfile, name='edit_profile'),  # Edit profile URL
    path('register/', views.Register, name='register' ),
    path('create-post/', views.Create_post, name='create_post'),
    path('post/<pk>/', views.Single_post, name='single_post'),  # Single post URL
    path('post-delete/<pk>/', views.Delete_post, name='delete_post'),
    path('post-edit/<pk>/', views.Edit_post, name='edit_post'),
    path('post/comment/<pk>', views.add_comment, name='add_comment'),
    path('delete-comment/<int:comment_id>/', views.delete_comment, name='comment-delete' ),
    path('post/<pk>/like', views.like_post, name='like-post'),
    path('search/', views.search, name='search'),
    path('reviews/<str:username>/', views.review_page, name='review_page'),
    path('toggle-favorite/<str:username>/', views.toggle_favorite, name='toggle_favorite'),
    path('favorite-list/', views.favorite_list, name='favorite_list'),
    path('private-feed/', views.private_feed, name='private_feed'),
    path('change-profile-picture/', views.change_profile_picture, name='change_profile_picture'),  # Profile picture URL
    path('', views.Login, name='login'),
    path('logout/', views.user_logout, name='logout'),  # Optional: Add logout functionality


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
