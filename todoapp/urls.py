from django.contrib import admin
from django.urls import include, path

api_urls = [
    path("", include("todos.urls")),
    path("", include("users.urls")),
    path("", include("projects.urls")),
]

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(api_urls)),
]
