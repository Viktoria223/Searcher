from django.urls import path

from web.views import main_view


urlpatterns = [
    path("search/", main_view, name="main")
]
