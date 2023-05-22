from django.urls import path
from .views import AddUserView, ReturnUserView, DeleteUserView, UpdateUserHometownView, UpdateUserInterestsView, TwitterTrackingView, LeaderboardView, QueryAllView, ConsumeAPI
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title='Endpoints for 0N1',
        default_version='v1',
        description='Important endpoints for the 0N1 Project',
        terms_of_service='https:www.example.comterms',
        contact=openapi.Contact(email='contact@example.com'),
        license=openapi.License(name='BSD License'),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path('adduser', AddUserView.as_view(), name='add_user'),
    path('row/<str:address>', ReturnUserView.as_view(), name='get_user_info'),
    path('deleterow/<str:address>', DeleteUserView.as_view(), name='delete_user_info'),
    path('updatehometown', UpdateUserHometownView.as_view(), name='update_user_hometown'),
    path('updateinterests', UpdateUserInterestsView.as_view(), name='update_user_interests'),
    path('leaderboardfetch', LeaderboardView.as_view(), name='fetch_leaderboard'),
    path('pfptracking', TwitterTrackingView.as_view(), name='twitter_tracking'),
    path('queryall/', QueryAllView.as_view(), name='get_user_info'),
    path('consume-api/<str:token_id>/<str:handle>/', ConsumeAPI.as_view(), name='consume-api'),
    # path('', views.home, name='home'),
    path('swagger', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
