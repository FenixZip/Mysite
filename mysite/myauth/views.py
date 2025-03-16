from django.contrib.auth.views import LogoutView
from django.urls import reverse_lazy
from django.views import View
from django.http import HttpResponse
from django.views.generic import CreateView
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import ProfileForm
from myauth.forms import RegisterForm
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404


class CustomLogoutView(LogoutView):
    """Logout с переадресацией на главную"""

    def dispatch(self, request, *args, **kwargs):
        """Перенаправляем пользователя после выхода"""
        response = super().dispatch(request, *args, **kwargs)
        return redirect("home")  # Главная страница


class ReadCookieView(View):
    """Чтение данных из cookies"""
    def get(self, request):
        favorite_color = request.COOKIES.get("favorite_color", "Не выбрано")
        return HttpResponse(f"Ваш любимый цвет: {favorite_color}")


class SetCookieView(View):
    """Установка данных в cookies"""
    def get(self, request):
        response = HttpResponse("Cookie установлена!")
        if not request.COOKIES.get("favorite_color"):
            response.set_cookie("favorite_color", "Синий", max_age=60*60*24)  # 1 день
        return response


class ReadSessionView(View):
    """Чтение данных из сессии"""
    def get(self, request):
        user_name = request.session.get("user_name", "Гость")
        return HttpResponse(f"Привет, {user_name}!")


class SetSessionView(View):
    """Установка данных в сессию"""
    def get(self, request):
        if "user_name" not in request.session:
            request.session["user_name"] = "Иван"
        return HttpResponse("Имя пользователя сохранено в сессии!")


class RegisterView(CreateView):
    """Регистрация пользователей"""
    model = User
    form_class = RegisterForm
    template_name = "myauth/register.html"
    success_url = reverse_lazy("home")  # После регистрации на главную страницу


from django.core.exceptions import PermissionDenied

@login_required
def about_me(request):
    """Страница профиля"""
    profile = request.user.profile

    if request.method == "POST":
        # Проверяем, что редактирует администратор или владелец профиля
        if not request.user.is_staff and request.user != profile.user:
            raise PermissionDenied()

        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect("myauth:about_me")
    else:
        form = ProfileForm(instance=profile)

    return render(request, "myauth/about_me.html", {"profile": profile, "form": form})


def user_list(request):
    """Список всех пользователей"""
    users = User.objects.all()
    return render(request, "myauth/user_list.html", {"users": users})

def user_profile(request, user_id):
    """Страница конкретного пользователя"""
    user = get_object_or_404(User, id=user_id)
    return render(request, "myauth/user_profile.html", {"user": user})

