from django.urls import path
from .views import *

app_name = 'api'
urlpatterns = [
    path('authenticated', CheckAuthenticated.as_view(), name='authenticated'),
    path('csrf-cookie', GetCSRFToken.as_view(), name='csrf-cookie'),
    path('register', SignUp.as_view(), name='register'),
    path('login', Login.as_view(), name='login'),
    path('logout', Logout.as_view(), name='logout'),
    path('delete', Delete.as_view(), name='delete'),
    path('users', GetUsers.as_view(), name='users'),
    path('profile', GetProfile.as_view(), name='profile'),
    path('other-profile', GetOtherProfile.as_view(), name='other-profile'),
    path('update', UpdateProfile.as_view(), name='update'),
    path('rate', Rate.as_view(), name='rate'),
    path('follow', Follow.as_view(), name='follow'),
    path('unfollow', Unfollow.as_view(), name='unfollow'),
    path('get-rating', GetRating.as_view(), name='get-rating'),
    path('get-ratings', GetFollowingRatings.as_view(), name='get-ratings'),
    path('like', LikeRating.as_view(), name='like'),
    path('comment', MakeComment.as_view(), name='comment')
]
