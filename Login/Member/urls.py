from django.urls import path
from Member.views import login, signup, logout, google, google_callback, index


urlpatterns = [
    path('member/login/', login),
    path('member/signup/', signup),
    path('member/logout/', logout),
    path('member/google/', google),
    path('member/google/callback/', google_callback),
    path('', index),
]
