from django.urls import path, include
from watchlist.api.views import (
    ReviewList,
    ReviewDetail,
    ReviewCreate,
    WatchListAV,
    MovieDetailsAV,
    StreamPlatformRV,
    UserReview)
from rest_framework.routers import DefaultRouter



router = DefaultRouter()
router.register('stream', StreamPlatformRV,basename='streamplatform') #not use as_view

urlpatterns = [
    path('list/', WatchListAV.as_view(), name='watchlist'),
    path('<int:pk>/', MovieDetailsAV.as_view(),name='movie-detail'),
    
    path('',include(router.urls)),
    
    path('review/<int:pk>', ReviewDetail.as_view(), name='review-detail'),
    path('<int:pk>/review/', ReviewList.as_view(), name='review-list'),
    path('<int:pk>/review-create/', ReviewCreate.as_view(), name='review-detail'),
    path('review/', UserReview.as_view(), name='user-review'),
]









