from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import RegisterView, LoginView, UserInfoView, StoryListView, StoryDetailView, add_contribution

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('user/', UserInfoView.as_view(), name='user_info'),
    path('stories/', StoryListView.as_view(), name='story_list'),
    path('stories/<int:pk>/', StoryDetailView.as_view(), name='story_detail'),
]   

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
