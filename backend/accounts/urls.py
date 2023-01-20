from django.urls import path
from .views import user_view, account_view

urlpatterns = [
    path('user/<int:pk>', user_view),
    path('account/', account_view),
]
