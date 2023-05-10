from django.urls import path
from . import views

urlpatterns = [
    path('category-list-create/', views.CategoryListCreate.as_view()),
    path('state-list-create/', views.StateListCreate.as_view()),
    path('<int:state_id>/region-list-create/', views.RegionListCreate.as_view()),
    path('region-rud/<int:pk>/', views.RegionRUD.as_view()),
    # path('<int:region_id>/company-list-create/', views.CompanyListCreate.as_view()),
    path('company-list-create/', views.CompanyListCreate.as_view()),
    path('company-rud/<int:pk>/', views.CompanyRUD.as_view()),
    path('type-list-create/', views.TypeListCreate.as_view()),
    path('tag-list-create/', views.TagListCreate.as_view()),
]
