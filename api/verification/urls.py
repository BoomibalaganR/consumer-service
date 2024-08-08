from django.urls import path

from .views import EmailVerificationView, ResendEmailVerificationView

urlpatterns = [
    path("email/verify-token", EmailVerificationView.as_view(), name="verify_email"),
    path(
        "email/resend-token",
        ResendEmailVerificationView.as_view(),
        name="resend_email_verification",
    ),
]
