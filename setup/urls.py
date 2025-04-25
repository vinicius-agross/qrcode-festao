
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from allauth.account.views import SignupView
from accounts.forms import CustomSignupForm


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('qrcode.urls')),
    path('accounts/', include('allauth.urls')),
    path('login/', auth_views.LoginView.as_view(template_name='cadastro/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', SignupView.as_view(
        template_name='cadastro/register.html',
        form_class=CustomSignupForm
    ), name='register'),
]
