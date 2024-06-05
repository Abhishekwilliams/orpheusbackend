from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAdminUser
from .models import BlogPost
from rest_framework import generics, mixins
from django.core.mail import send_mail
from .serializers import UserSerializer, BlogPostSerializer, EmailSerializer

class SignupAPIView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginAPIView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user:
            return Response({'token': 'your_token_here'}, status=status.HTTP_200_OK)
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

class BlogPostListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = BlogPostSerializer
    queryset = BlogPost.objects.all()
    permission_classes = (AllowAny,)
    
    # admin user
    # def get_permissions(self):
    #     permissions = super().get_permissions()

    #     if self.request.method.lower() == 'post':
    #         permissions.append(IsAdminUser())
    #     return permissions

class BlogPostDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = BlogPostSerializer
    queryset = BlogPost.objects.all()
    
class SendEmail(APIView):
    def post(self, request, *args, **kwargs):
        serializer = EmailSerializer(data=request.data)
        if serializer.is_valid():
            name = serializer.validated_data.get('name')
            email = serializer.validated_data.get('email')
            message = serializer.validated_data.get('message')
            try:
                # Compose and send email
                send_mail(
                    f"Message from {name}",
                    f"Email: {email}\n\nMessage: {message}",
                    email,  # Sender's email
                    ['gptwilliams5@gmail.com'],  # Recipient's email
                    fail_silently=False,
                )
                return Response({'message': 'Email sent successfully'}, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({'error': f"Failed to send email: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)