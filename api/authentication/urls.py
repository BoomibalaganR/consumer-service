from django.urls import path
from .views import ConsumerRegisterView, LoginView

urlpatterns = [
    path('register', ConsumerRegisterView.as_view(), name='consumer-register'), # type: ignore
    path('login', LoginView.as_view(), name='login'),
#     
# path('forgot-password/', ForgotPasswordView.as_view(), name='forgot_password'),
#     path('verify-password-token/', VerifyPasswordTokenView.as_view(),
#          name='verify_password_token'),
#     path('resend-password-token/', ResendPasswordTokenView.as_view(),
#          name='resend_password_token'),
]
