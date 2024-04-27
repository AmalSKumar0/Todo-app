from django.urls import path
from . import views

urlpatterns = [
    path('',views.home , name="home"),
    path('login/',views.loginPage , name="login"),
    path('createtask/',views.createtask, name="createTask"),
    path('lists/<str:pk>/',views.listRoom, name="Lists"),
    path('update/', views.update, name="update"), 
    path('delete-item/<int:item_id>/', views.delete_item, name='delete_item'),
    path('delete/<int:item_id>/', views.dele, name='delete_item_hehe'),
    path('register/', views.register, name='register'),
]
