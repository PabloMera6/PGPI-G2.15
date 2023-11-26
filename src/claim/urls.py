from django.urls import path
from .views import create_claim, view_claims, view_claim, user_view_claims, user_view_claim

urlpatterns = [
    path('create_claim/', create_claim, name='create_claim'),
    path('view_claims/', view_claims, name='view_claims'),
    path('view_claim/<int:claim_id>/', view_claim, name='view_claim'),
    path('user_view_claims/', user_view_claims, name='user_view_claims'),
    path('user_view_claim/<int:claim_id>/', user_view_claim, name='user_view_claim'),
]
