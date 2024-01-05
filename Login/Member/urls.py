from django.urls import path
from Member.views import login, signup, logout, index


urlpatterns = [
    path('member/login/', login),
    path('member/signup/', signup),
    path('member/logout/', logout),
    path('', index),
]
