from django.contrib.auth import views as auth_views
from django.urls import path
from .views import signup, activate

urlpatterns = [
    path('signup/', signup, name='signup'),
    path('activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/',
         activate, name='activate'),
    path('login/', auth_views.LoginView.as_view(next_page='announcements'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='registration/logged_out.html'),
         name='logout'),
]
