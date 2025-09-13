from django.urls import path
from . import views

urlpatterns = [
    path('', views.inbox, name='bin_inbox'),
    path('conversation/<int:pk>/', views.conversation_detail, name='bin_conversation'),
    path('conversation/new/<int:user_id>/', views.start_conversation_with, name='bin_start_with'),
    path('conversation/<int:pk>/send/', views.send_message, name='bin_send_message'),
    path('conversation/<int:pk>/delete/', views.delete_conversation, name='bin_delete_conversation'),
    path("search/", views.search_users, name="bin_search"),

]
