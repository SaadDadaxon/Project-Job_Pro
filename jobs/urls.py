from django.urls import path
from . import views


urlpatterns = [
    path('job-list-create/', views.JobsListCreate.as_view()),
    path('like-list-create/<int:jobs_id>/', views.LikeListCreate.as_view()),
    path('apply-candidate-create/', views.ApplyCreate.as_view()), # Candidate Create qiladi buni
    path('apply-job-list-isadmin/', views.ApplyJobList.as_view()),
    path('apply-list-hr/<int:jobs_id>/', views.ApplyList.as_view()), # HR ko'radi buni
]

