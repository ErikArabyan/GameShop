from django.urls import path
from .views import *
from django.contrib.auth import views

urlpatterns = [
    path('home/', home, name = 'home'),
    path('', home, name = 'home'),
    path('details/<int:id>/', details, name = 'details'),
    path('contact-us/', contact, name = 'contact'),
    path('shop/', shop, name = 'shop'),
    path('personal_account/', personal_account, name = 'personal_account'),

    path('register/', Register, name = 'register'),
    path('verify_email/<uidb64>/<token>/', Emailverify, name='verify_email'),
    path('change_email/<uidb64>/<token>/', ChangeEmail, name='change_email'),
    path('confirm_email/', confirm_email, name='confirm_email'),

    path('logout/', Logout, name = 'logout'),

    path('password_reset/', views.PasswordResetView.as_view(template_name='password_reset_form.html'), name='password_reset'),
    path('password_reset_done/', views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'), name='password_reset_done'),
    path('password_reset_confirm/<uidb64>/<token>/',views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'), name='password_reset_confirm'),
    path('password_reset_complete/', views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), name='password_reset_complete'),
]