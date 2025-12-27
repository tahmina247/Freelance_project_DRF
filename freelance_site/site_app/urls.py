from django.urls import path, include
from rest_framework import routers
from .views import *


router = routers.SimpleRouter()
router.register(r'users/me', UserProfileViewSet, basename='users')


urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),

    path('', include(router.urls)),
    path('category/', CategoryListAPIView.as_view(), name='category_list'),
    path('category/<int:pk>/', CategoryDetailAPIView.as_view(), name='category_detail'),
    path('project/', ProjectAPIView.as_view(), name='project_list'),
    path('project/<int:pk>/', ProjectDetailAPIView.as_view(), name='project_detail'),
    path('project/create/', ProjectPostApiView.as_view(), name='project_create'),
    path('project/create/<int:pk>/', ProjectEditAPIView.as_view(), name='project_edit'),
    path('project/my/', ProjectMyAPIView.as_view(), name='project_client'),
    # path('offer/<int:pk>/', OfferDetailAPIView.as_view(), name='offer_detail'),
    path('offer/my', OfferListAPIView.as_view(), name='offer_list'),
    path('offer/create/', OfferCreateAPIView.as_view(), name='offer_create'),
    path('offer/my/<int:pk>/', OfferEditAPIView.as_view(), name='offer_edit'),
    path('review/', ReviewAPIView.as_view(), name='review_list'),
    path('review/<int:pk>/', ReviewDetailAPIView.as_view(), name='review_detail'),
    path('review/create/', ReviewCreateAPIView.as_view(), name='review_create'),
    path('users/', UserProfileListAPIView.as_view(), name='users_list'),
    path('users/<int:pk>/', UserProfileDetailAPIView.as_view(), name='user_detail'),
    ]