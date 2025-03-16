from django.contrib import admin
from django.urls import include, path

api_urls = [
    path("todos/", include("todos.urls")),
    path("", include("users.urls")),
    path("projects/", include(("projects.urls", "projects"))),
]

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(api_urls)),
]
