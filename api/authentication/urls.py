from django.urls import path

from .views import (
    ConsumerRegisterView,
    ForgotPasswordView,
    LoginView,
    ResendPasswordTokenView,
    VerifyPasswordTokenView,
)

urlpatterns = [
    path("register", ConsumerRegisterView.as_view(), name="consumer-register"),  # type: ignore
    path("login", LoginView.as_view(), name="login"),
    # Password reset endpoints
    path("email/forgot-password", ForgotPasswordView.as_view(), name="forgot_password"),
    path(
        "email/verify-password-token",
        VerifyPasswordTokenView.as_view(),
        name="verify_password_token",
    ),
    path(
        "email/resend-password-token",
        ResendPasswordTokenView.as_view(),
        name="resend_password_token",
    ),
]
