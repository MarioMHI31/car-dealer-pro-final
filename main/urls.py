from django.urls import path
from . import views
from django.contrib.auth import views as auth_views  # ✅ Import corect
from django.contrib.auth.decorators import login_required  # ✅ Import corect

urlpatterns = [
    path('', views.home, name='home'),
    path('search/', views.search, name='search'),
    path('sell/', login_required(views.sell), name='sell'),
    path('ads/', views.ads, name='ads'),
    path('ads/<int:car_id>/', views.ad_detail, name='ad_detail'),
    path('login/', auth_views.LoginView.as_view(template_name='main/login.html'), name='login'),
    path('signup/', views.signup, name='signup'),
    path('profile/', views.profile_view, name='profile'),
    path('edit-profile/', views.edit_profile, name='edit_profile'),
    path('logout/', views.logout_view, name='logout'),
    path('favorites/', views.favorites_view, name='favorites'),
    path('toggle-favorite/', views.toggle_favorite, name='toggle_favorite'),
    path("ad/<int:car_id>/delete/", views.delete_car, name="delete_car"),
    path('confirm-email/', views.confirm_email_before_password_change, name='confirm_email'),
    path('confirm-code/', views.confirm_code_view, name='confirm_code'),
    path('reset-password/', views.reset_password_view, name='reset_password'),




]

