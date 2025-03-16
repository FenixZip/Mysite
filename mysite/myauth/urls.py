from django.conf.urls.static import static
from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from myauth.views import (
    RegisterView, ReadCookieView, SetCookieView, ReadSessionView, SetSessionView, about_me, user_list, user_profile
)
from mysite import settings

app_name = "myauth"

urlpatterns = [
    path("login/", LoginView.as_view(
        template_name="myauth/login.html",
        redirect_authenticated_user=True
    ), name="login"),

    path("logout/", LogoutView.as_view(next_page="home"), name="logout"),  # Используем стандартный LogoutView

    path("register/", RegisterView.as_view(), name="register"),

    path("read-cookie/", ReadCookieView.as_view(), name="read_cookie"),
    path("set-cookie/", SetCookieView.as_view(), name="set_cookie"),
    path("read-session/", ReadSessionView.as_view(), name="read_session"),
    path("set-session/", SetSessionView.as_view(), name="set_session"),
    path("about-me/", about_me, name="about_me"),
    path("users/", user_list, name="user_list"),
    path("users/<int:user_id>/", user_profile, name="user_profile"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
