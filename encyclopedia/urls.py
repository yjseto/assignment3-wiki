from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path('search/', views.search, name="search"),
    path("new/", views.new, name="new"),
    path("edit/<str:title>", views.edit, name="edit"),
    path("random", views.random_entry, name="random"),
    path("<str:entry>", views.title, name="title"),
    path("delete/<str:title>", views.delete, name="delete")
]
