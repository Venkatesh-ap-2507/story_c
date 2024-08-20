from rest_framework import generics,permissions
from .models import User, Story
from .serializers import UserSerializer,StorySerializer
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import api_view,permission_classes
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from rest_framework.permissions import AllowAny


from rest_framework import status
from django.utils.functional import SimpleLazyObject
from rest_framework.exceptions import ValidationError

class RegisterView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        if not username or not password:
            return Response({'error': 'Username and password are required.'}, status=status.HTTP_400_BAD_REQUEST)
        if User.objects.filter(username=username).exists():
            return Response({'error': 'Username already taken.'}, status=status.HTTP_400_BAD_REQUEST)
        user = User(username=username, password=make_password(password))
        user.save()

        return Response({
            'user': UserSerializer(user).data,
            'message': 'User created successfully.'
        }, status=status.HTTP_201_CREATED)


class LoginView(generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')

        # Use the plain password for authentication
        user = authenticate(username=username, password=password)

        if user:
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

class UserInfoView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        if request.user.is_authenticated:
            return Response(UserSerializer(request.user).data)
        else:
            return Response({'error': 'User not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)

class StoryListView(generics.ListCreateAPIView):
   queryset = Story.objects.all()
   serializer_class = StorySerializer
   permission_classes = [permissions.IsAuthenticated]

   def perform_create(self, serializer):
      user = self.request.user
      if isinstance(user, SimpleLazyObject):
        user = user._wrapped  # Unwrap the SimpleLazyObject
      if User.objects.filter(id=user.id).exists():  # Check if the user exists
        serializer.save(created_by_id=user.id)
      else:
        raise ValidationError("User does not exist")
        
class StoryDetailView(generics.RetrieveAPIView):
    queryset = Story.objects.all()
    serializer_class = StorySerializer
    permission_classes = [permissions.IsAuthenticated]


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def add_contribution(request, pk):
    try:
        story = Story.objects.get(pk=pk)
    except Story.DoesNotExist:
        return Response({'error': 'Story not found.'}, status=404)

    content = request.data.get('content')
    if not content:
        return Response({'error': 'Content cannot be empty.'}, status=400)

    story.contributions.append({'user_id': request.user.id, 'content': content})
    story.save()
    return Response(StorySerializer(story).data)