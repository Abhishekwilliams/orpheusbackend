from django.urls import path
from .views import SignupAPIView, LoginAPIView,BlogPostListCreateAPIView,BlogPostDetailAPIView,SendEmail

urlpatterns = [
    path('signup/', SignupAPIView.as_view(), name='signup'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('send-email/', SendEmail.as_view(), name='send_email'),
    path('blog/<int:pk>/',BlogPostDetailAPIView.as_view(),name='blog-detail'),
    path('blog/',BlogPostListCreateAPIView.as_view(),name='blog'),
]