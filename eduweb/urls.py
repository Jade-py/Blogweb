from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('users.urls')),
    path('account/', include('django.contrib.auth.urls')),
    path('auth/', include('social_django.urls', namespace='social')),
    path('workspace/', include('workspace.urls')),
    path('tinymce/', include('tinymce.urls')),
]
