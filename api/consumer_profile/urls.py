# consumers/urls.py
from django.urls import path

from .views import ConsumerProfileView

urlpatterns = [
    path("", ConsumerProfileView.as_view(), name="consumer-profile-detail"),
]
