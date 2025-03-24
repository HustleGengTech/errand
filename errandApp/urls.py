from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import handler404
from django.shortcuts import render
from django.contrib.auth import views as auth_views
from .views import change_email, CustomPasswordChangeView
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
    path('settings/', views.settings, name='settings'),
    path('change-profile-picture/', views.change_profile_picture, name='change_profile_picture'),  # Profile picture URL
    path('', views.Login, name='login'),
    path('logout/', views.user_logout, name='logout'),  # Optional: Add logout functionality
    path('change-email/', change_email, name='change_email'),
    path('change-password/', CustomPasswordChangeView.as_view(), name='change_password'),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='password_reset.html'), name='password_reset'),
    
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='password_reset_done.html'
    ), name='password_reset_done'),
    
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='password_reset_confirm.html'
    ), name='password_reset_confirm'),
    
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name='password_reset_complete.html'
    ), name='password_reset_complete'),
    path('write-to-us/', views.write_to_us, name='write_to_us'),
    path('thank-you/', views.thank_you, name='thank_you'),
    path('filter-posts/', views.filter_posts, name='filter_posts'),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



def custom_404(request, exception):
    return render(request, '404.html', status=404)

handler404 = custom_404
