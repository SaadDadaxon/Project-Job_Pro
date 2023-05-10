from django.urls import path
from . import views

urlpatterns = [
    path('list-create/', views.BlogListCreate.as_view()),
    path('rud/<int:pk>/', views.BlogRUD.as_view()),
    path('<int:blog_id>/comment-list-create/', views.CommentListCreate.as_view()),
]
