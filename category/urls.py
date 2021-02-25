from django.urls import path
from .views import (
    CategoriesList, CategoriesDetails, CategoryLeadUpdate, CategoriesCreate,
    CategoriesUpdate, CategoriesDelete
)

app_name = "category"

urlpatterns = [
    path('', CategoriesList.as_view(), name='category-list'),
    path('create', CategoriesCreate.as_view(), name='category-create'),
    path('update/<int:pk>',
         CategoriesUpdate.as_view(), name='category-update'),
    path('delete/<int:pk>',
         CategoriesDelete.as_view(), name='category-delete'),
    path('details/<int:pk>', CategoriesDetails.as_view(),
         name='category-details'),
]
