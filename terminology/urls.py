from django.urls import path
from .views import RefbookListView, ElementListView, ValidateElementView

urlpatterns = [
    path('refbooks/', RefbookListView.as_view(), name='refbook-list'),
    path('refbooks/<int:id>/elements/', ElementListView.as_view(), name='refbook-elements'),
    path('refbooks/<int:id>/check_element/', ValidateElementView.as_view(), name='validate-element'),
]
