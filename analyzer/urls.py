from django.urls import path
from . import views

urlpatterns = [
    path("", views.home_view, name="home"),
    path("history/", views.history_view, name="history"),
    path("delete_resume/<int:id>", views.delete_resume, name="delete_resume"),
    path("delete_all/", views.delete_all, name="delete_all"),
    path("resume/<int:id>/", views.resume_details, name="resume_detail"),
]
