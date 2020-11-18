from django.urls import path
from blog import api

urlpatterns = [
    path("api/blog-list", api.blog_list_view, name="blog-list"),
    path("api/blog-detail/<slug>", api.blog_detail_view, name="blog-detail"),
]