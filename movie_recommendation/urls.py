from django.conf import settings
from . import views
from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.home, name="home"),
    path("recommend/", views.recommend, name="recommend"),
    path("ranking/", views.ranking, name="ranking"),
    # path("ranking/<topic>", views.ranking, name="ranking"),
    # ---------------------------------------------------------------------- H T M X ------------------------------------------------------------------
    path("htmx_search_results/", views.htmx_search_results, name="htmx_search_results"),
    path("htmx_desc/<str:title>", views.htmx_desc, name="htmx_desc"),
    # path("htmx_ranking_results/", views.htmx_ranking_results, name="htmx_ranking_results"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
