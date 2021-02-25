from django.urls import path
from leads.views import (
    LeadList, LeadDetails, LeadCreate, LeadUpdate, LeadDelete, LeadUnassignedList,
    AssignAgent, FollowUpCreate, FollowUpDelete, FollowUpUpdate
)

app_name = "leads"

urlpatterns = [
    path('', LeadList.as_view(), name='lead-list'),
    path('unassigned/', LeadUnassignedList.as_view(), name='unassigned-leads'),
    path('<int:pk>/', LeadDetails.as_view(), name='lead-details'),
    path('<int:pk>/update/', LeadUpdate.as_view(), name='lead-update'),
    path('<int:pk>/delete/', LeadDelete.as_view(), name='lead-delete'),
    path('<int:pk>/assign_agent/', AssignAgent.as_view(), name='lead-agent'),
    path('<int:pk>/following_up/create',
         FollowUpCreate.as_view(), name='lead-follow-create'),
    path('<int:pk>/following_up/update',
         FollowUpUpdate.as_view(), name='lead-follow-update'),
    path('<int:pk>/following_up/delete',
         FollowUpDelete.as_view(), name='lead-follow-delete'),
    path('create/', LeadCreate.as_view(), name='lead-create'),
]
