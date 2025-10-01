# django files
from django.urls import path, include

# rest files
from rest_framework.routers import DefaultRouter

# your files
from .views import UserViewSet, ContactViewSet, SocialLinkViewSet

app_name = 'accounts'

router = DefaultRouter()
router.register('users', UserViewSet, basename='users')
router.register(r'contacts', ContactViewSet, basename='contact')
router.register(r'social/links', SocialLinkViewSet, basename='social-link')
urlpatterns = [
    path('', include(router.urls)),
]