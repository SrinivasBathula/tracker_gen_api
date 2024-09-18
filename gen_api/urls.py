from django.urls import path, include
from .views import NextTrackingNumberView


urlpatterns = [
    path(
        "next-tracking-number/",
        NextTrackingNumberView.as_view(),
        name="next-tracking-number",
    ),
]
