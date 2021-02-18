from django.urls import path
from .views import AgentsList, AgentsCreate, AgentDetails, AgentUpdate, AgentDelete


app_name = "agents"

urlpatterns = [
    path('', AgentsList.as_view(), name='agent_list'),
    path('create', AgentsCreate.as_view(), name='agent_create'),
    path('<int:pk>/', AgentDetails.as_view(), name='agent_details'),
    path('<int:pk>/update/', AgentUpdate.as_view(), name='agent_update'),
    path('<int:pk>/delete/', AgentDelete.as_view(), name='agent_delete'),
]
