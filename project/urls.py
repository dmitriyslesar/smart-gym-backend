from django.contrib import admin
from django.urls import path
from app.views import (
    UserListView, UserProfileView, RegApiView, 
    AuthApiView, OrderListApi, DeleteOrderApi, CreateOrderApi
)
from django.http import JsonResponse

def home_view(request):
    return JsonResponse({
        "status":"healthy",
        "project":"Smart Gym",
        "version":"1.0"
    })

urlpatterns = [
    path('', home_view, name='home'),
    path('admin/', admin.site.urls),
    path('list/', UserListView.as_view()),
    path('profile/', UserProfileView.as_view()),
    path('register/', RegApiView.as_view()),
    path('login/', AuthApiView.as_view()),
    path('orders/', OrderListApi.as_view()),
    path('orders/create/', CreateOrderApi.as_view()),
    path('orders/delete/<int:pk>/', DeleteOrderApi.as_view()),
]