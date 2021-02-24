import random
from crm.mail import sendEmail
from crm.email_templates import welcomePasswordEmail
from django.shortcuts import redirect, reverse
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from leads.models import Agent
from .forms import AgentModelForm
from .mixins import OrganiserAndLoginMixin


class AgentsList(OrganiserAndLoginMixin, ListView):
    template_name = 'agents/agent_list.html'
    context_object_name = 'agents'

    def get_queryset(self):
        request_user_organisation = self.request.user.userprofile
        return Agent.objects.filter(organisation=request_user_organisation)


class AgentsCreate(OrganiserAndLoginMixin, CreateView):
    template_name = 'agents/agent_create.html'
    form_class = AgentModelForm

    def get_success_url(self):
        return reverse("agents:agent_list")

    def form_valid(self, form):
        password = f"{random.randint(0, 1000000)}"
        user = form.save(commit=False)
        user.is_agent = True
        user.is_organiser = False
        user.set_password(password)
        user.save()
        Agent.objects.create(
            user=user,
            organisation=self.request.user.userprofile
        )

        sendEmail(user, welcomePasswordEmail(
            user, password), 'Welcome to Lead CRM')

        return super(AgentsCreate, self).form_valid(form)


class AgentDetails(OrganiserAndLoginMixin, DetailView):
    template_name = 'agents/agent_details.html'
    context_object_name = 'agent'

    def get_queryset(self):
        request_user_organisation = self.request.user.userprofile
        return Agent.objects.filter(organisation=request_user_organisation)


class AgentUpdate(OrganiserAndLoginMixin, UpdateView):
    template_name = 'agents/agent_update.html'
    form_class = AgentModelForm

    def get_queryset(self):
        user = self.request.user
        if user.is_organiser:
            queryset = Agent.objects.filter(
                organisation=user.userprofile)
        return queryset

    def get_success_url(self):
        return reverse("agents:agent_list")


class AgentDelete(OrganiserAndLoginMixin, DeleteView):
    template_name = 'agents/agent_delete.html'

    def get_success_url(self):
        return reverse("agents:agent_list")

    def get_queryset(self):
        request_user_organisation = self.request.user.userprofile
        return Agent.objects.filter(organisation=request_user_organisation)
