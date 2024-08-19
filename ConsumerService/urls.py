"""
URL configuration for ConsumerService project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import include, path

urlpatterns = [
    path("api/v1/consumers/auth/", include("api.authentication.urls")),
    path("api/v1/consumers/profile/", include("api.consumer_profile.urls")),
    path("api/v1/consumers/verification/", include("api.verification.urls")),
    path("api/v1/consumers/relationships/", include("api.relationship.urls")),
]
