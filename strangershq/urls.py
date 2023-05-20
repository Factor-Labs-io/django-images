from django.urls import path
from strangershq import views
from .views import AddUserView, ReturnUserView, DeleteUserView, UpdateUserHometownView, UpdateUserInterestsView, TwitterTrackingView, LeaderboardView
from drf_yasg import views as yasg_views
from drf_yasg import openapi
from rest_framework import permissions

schema_view = yasg_views.get_schema_view(
    openapi.Info(
        title='Endpoints for StrangersHQ',
        default_version='v1',
        description='Important endpoints for the SHQ Project',
        terms_of_service='https://www.example.com/terms/',
        contact=openapi.Contact(email='contact@example.com'),
        license=openapi.License(name='BSD License'),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path('adduser/', AddUserView.as_view(), name='add_user'),
    path('row/', ReturnUserView.as_view(), name='get_user_info'),
    path('deleterow/', DeleteUserView.as_view(), name='delete_user_info'),
    path('updatehometown/', UpdateUserHometownView.as_view(), name='update_user_hometown'),
    path('updateinterests/', UpdateUserInterestsView.as_view(), name='update_user_interests'),
    path('leaderboardfetch/', LeaderboardView.as_view(), name='fetch_leaderboard'),
    path('twittertracking/', TwitterTrackingView.as_view(), name='twitter_tracking'),
    path('', views.home, name='home'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
