from api.relationship.views import (
    AcceptRelationshipView,
    CreateRelationshipView,
    GetRelationshipsByIdView,
    ListRelationshipsView,
    TagCountView,
)
from django.urls import path

urlpatterns = [
    path(
        "",
        ListRelationshipsView.as_view(),
        name="list-relationships",
    ),
    path("tagcount", TagCountView.as_view(), name="relationship-tag-count"),
    path(
        "request",
        CreateRelationshipView.as_view(),
        name="create-relationship",
    ),
    path(
        "<str:rel_id>",
        GetRelationshipsByIdView.as_view(),
        name="get-relationship-By-id",
    ),
    path(
        "<str:rel_id>/accept",
        AcceptRelationshipView.as_view(),
        name="accept-relationship",
    ),
]
