from django.urls import path

from leads.views import (
    LeadList, LeadDetails, LeadCreate, LeadUpdate, LeadDelete, AssignAgent,
    CategoriesList, CategoriesDetails, CategoryLeadUpdate, CategoriesCreate,
    CategoriesUpdate,
)

app_name = "leads"

urlpatterns = [
    path('', LeadList.as_view(), name='lead-list'),
    path('<int:pk>/', LeadDetails.as_view(), name='lead-details'),
    path('<int:pk>/update/', LeadUpdate.as_view(), name='lead-update'),
    path('<int:pk>/delete/', LeadDelete.as_view(), name='lead-delete'),
    path('<int:pk>/assign_agent/', AssignAgent.as_view(), name='lead-agent'),
    path('<int:pk>/update_category/',
         CategoryLeadUpdate.as_view(), name='lead-category'),
    path('create/', LeadCreate.as_view(), name='lead-create'),
    path('create/category', CategoriesCreate.as_view(), name='category-create'),
    path('create/update/<int:pk>',
         CategoriesUpdate.as_view(), name='category-update'),
    path('create/delete/<int:pk>',
         CategoriesCreate.as_view(), name='category-delete'),
    path('categories/', CategoriesList.as_view(), name='category-list'),
    path('<int:pk>/categories', CategoriesDetails.as_view(),
         name='category-details'),
]
