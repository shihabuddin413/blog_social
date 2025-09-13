from django.urls import path
from . import views

from django.contrib.auth import views as auth_views


urlpatterns = [
    path ('', views.home, name='home'),
    path ('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('post/new/', views.create_post, name='create_post'),
    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('post/<int:pk>/edit/', views.edit_post, name='edit_post'),
    path('post/<int:pk>/delete/', views.delete_post, name='delete_post'),
    path('post/<int:pk>/comment/', views.add_comment, name='add_comment'),
    path('post/<int:pk>/like/', views.toggle_like, name='toggle_like'),
    path('post/<int:pk>/requote/', views.requote_post, name='requote_post'),
    path('requote/<int:pk>/delete/', views.delete_requote, name='delete_requote'),
    path('profile/activity/', views.activity_page, name='activity_page'),
    path('profile/activity/delete/<int:pk>/<str:activity_type>/', views.delete_activity, name='delete_activity' ),


    #auth urls

    path ('login/',
          views.CustomLoginView.as_view(next_page='home'),
          name = 'login'),

    path ('logout/',
          auth_views.LogoutView.as_view
              ( next_page = 'home' ),
          name = 'logout'),

    path ('signup', views.signup, name='signup'),
]