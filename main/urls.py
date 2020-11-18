from django.conf import settings
from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static
from rest_framework.authtoken import views
from blog import api

urlpatterns = [
    path('admin/', admin.site.urls),
    path('blog/', include("blog.urls")),
    path('api/accounts/', api.CustomAuthToken.as_view())
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)