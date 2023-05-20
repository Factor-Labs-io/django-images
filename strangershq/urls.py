from django.urls import path
from strangershq import views
from .views import AddUserView, ReturnUserView, DeleteUserView, UpdateUserHometownView, UpdateUserInterestsView, TwitterTrackingView, LeaderboardView

urlpatterns = [
    path('adduser/', AddUserView.as_view(), name='add_user'),
    path('row/', ReturnUserView.as_view(), name='get_user_info'),
    path('deleterow/', DeleteUserView.as_view(), name='delete_user_info'),
    path('updatehometown/', UpdateUserHometownView.as_view(), name='update_user_hometown'),
    path('updateinterests/', UpdateUserInterestsView.as_view(), name='update_user_interests'),
    path('leaderboardfetch/', LeaderboardView.as_view(), name='fetch_leaderboard'),
    path('twittertracking/', TwitterTrackingView.as_view(), name='twitter_tracking'),
    path('', views.home, name='home'),
]
