from django.urls import path
from . import views

urlpatterns = [
    path("", views.MainView.as_view()),
    path("worker/auth", views.ProfileLogin.as_view()),
    path("client/auth", views.ProfileLogin.as_view()),
    path("client/registration", views.NewProfile.as_view()),
    path("logout", views.ProfileLogout.as_view()),
    path("task", views.TaskCreate.as_view()),
    path("task/<int:pk>", views.TaskInProcess.as_view()),
    path("task-done/<int:pk>", views.TaskDone.as_view()),
    path("client", views.ClientList.as_view()),
    path("worker/", views.WorkerList.as_view()),
    path("worker/<int:pk>", views.WorkerListId.as_view()),
]
