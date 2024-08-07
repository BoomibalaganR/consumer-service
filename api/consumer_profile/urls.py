# consumers/urls.py
from django.urls import path
from .views import ConsumerProfileDetailView

urlpatterns = [
    path('', ConsumerProfileDetailView.as_view(), name='consumer-profile-detail'),
]
