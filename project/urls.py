from django.contrib import admin
from django.urls import path
from app.views import UserListView, UserProfileView, RegApiView, AuthApiView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('list/', UserListView.as_view()),
    path('profile/', UserProfileView.as_view()),
    path('register/', RegApiView.as_view()),
    path('login/', AuthApiView.as_view()),
]
