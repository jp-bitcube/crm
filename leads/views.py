from django.shortcuts import render, redirect, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView, FormView
from .models import Lead, Agent, Category, FollowUp
from .forms import LeadModelForm, LeadForm, AssignAgentForm, FollowUpModelForm
from agents.mixins import OrganiserAndLoginMixin
from django.contrib.auth.views import PasswordResetView
from crm.mail import sendEmail
from crm.email_templates import assignedLead
from category.forms import CategoryForm


class LeadList(LoginRequiredMixin, ListView):
    template_name = 'leads/lead_list.html'
    context_object_name = 'leads'
    paginate_by = 5

    def get_queryset(self):
        user = self.request.user
        if self.request.user.is_organiser:
            queryset = Lead.objects.filter(
                organisation=user.userprofile, agent__isnull=False)
        else:
            queryset = Lead.objects.filter(
                organisation=user.agent.organisation, agent__isnull=False)
            queryset = queryset.filter(agent__user=user)
        return queryset

    def get_context_data(self, **kwargs):
        user = self.request.user
        context = super(LeadList, self).get_context_data(**kwargs)
        if user.is_organiser:
            queryset = Lead.objects.filter(
                organisation=user.userprofile, agent__isnull=True)
            context.update({
                "unassigned_leads": queryset
            })
        return context


class LeadUnassignedList(OrganiserAndLoginMixin, ListView):
    template_name = 'leads/lead_unassigned_list.html'
    context_object_name = 'leads'
    paginate_by = 5

    def get_queryset(self):
        user = self.request.user
        if user.is_organiser:
            queryset = Lead.objects.filter(
                organisation=user.userprofile, agent__isnull=True)
        return queryset


class LeadDetails(LoginRequiredMixin, DetailView):
    template_name = 'leads/lead_details.html'
    context_object_name = 'lead'

    def get_queryset(self):
        user = self.request.user
        if self.request.user.is_organiser:
            queryset = Lead.objects.filter(
                organisation=user.userprofile)
        else:
            queryset = Lead.objects.filter(
                organisation=user.agent.organisation)
            queryset = queryset.filter(agent__user=user)
        return queryset


class LeadCreate(OrganiserAndLoginMixin, CreateView):
    template_name = 'leads/lead_create.html'
    form_class = LeadModelForm
    loading = False

    def get_success_url(self):
        return reverse("leads:lead-list")

    def form_valid(self, form):
        loading = True
        if (loading):
            lead = form.save(commit=False)
            lead.organisation = self.request.user.userprofile
            lead.save()

            if lead.agent:
                sendEmail(lead.agent.user, assignedLead(
                    lead.agent.user), 'Assigned Lead')

            return super(LeadCreate, self).form_valid(form)


class LeadUpdate(OrganiserAndLoginMixin, UpdateView):
    template_name = 'leads/lead_update.html'
    form_class = LeadModelForm

    def get_queryset(self):
        user = self.request.user
        if user.is_organiser:
            queryset = Lead.objects.filter(
                organisation=user.userprofile)
        else:
            queryset = Lead.objects.filter(
                organisation=user.agent.organisation)
        return queryset

    def get_success_url(self):
        return reverse("leads:lead-list")


class LeadDelete(OrganiserAndLoginMixin, DeleteView):
    template_name = 'leads/lead_delete.html'

    def form_valid(self, form):
        user = self.request.user
        lead = Lead.objects.get(id=pk)
        lead.delete()
        return super(LeadDelete, self).form_valid(form)

    def get_success_url(self):
        return reverse("leads:lead-list")

    def get_queryset(self):
        user = self.request.user
        # initial queryset of leads for the entire organisation
        return Lead.objects.filter(organisation=user.userprofile)


class AssignAgent(OrganiserAndLoginMixin, FormView):
    template_name = 'leads/assign_view.html'
    form_class = AssignAgentForm

    def get_success_url(self):
        return reverse("leads:lead-list")

    def get_form_kwargs(self, **kwargs):
        kwargs = super(AssignAgent, self).get_form_kwargs(**kwargs)
        kwargs.update({
            "request": self.request
        })
        return kwargs

    def form_valid(self, form):
        agent = form.cleaned_data["agent"]
        lead = Lead.objects.get(id=self.kwargs["pk"])
        lead.agent = agent
        lead.save()
        return super(AssignAgent, self).form_valid(form)

    template_name = 'leads/lead_category_details.html'
    context_object_name = 'category'
    form_class = CategoryForm

    def get_success_url(self):
        return reverse("leads:lead-details", kwargs={"pk": self.get_object().id})

    def get_queryset(self):
        user = self.request.user
        if user.is_organiser:
            queryset = Lead.objects.filter(
                organisation=user.userprofile)
        else:
            queryset = Lead.objects.filter(
                organisation=user.agent.organisation)
        return queryset


class FollowUpCreate(LoginRequiredMixin, CreateView):
    template_name = "leads/followup_create.html"
    form_class = FollowUpModelForm

    def get_success_url(self):
        return reverse("leads:lead-details", kwargs={"pk": self.kwargs["pk"]})

    def get_context_data(self, **kwargs):
        context = super(FollowUpCreate, self).get_context_data(**kwargs)
        context.update({
            "lead": Lead.objects.get(pk=self.kwargs["pk"])
        })
        return context

    def form_valid(self, form):
        lead = Lead.objects.get(pk=self.kwargs["pk"])
        followup = form.save(commit=False)
        followup.lead = lead
        followup.save()
        return super(FollowUpCreate, self).form_valid(form)


class FollowUpUpdate(LoginRequiredMixin, UpdateView):
    template_name = "leads/followup_update.html"
    form_class = FollowUpModelForm

    def get_queryset(self):
        user = self.request.user
        if user.is_organiser:
            queryset = FollowUp.objects.filter(
                lead__organisation=user.userprofile)
        else:
            queryset = FollowUp.objects.filter(
                lead__organisation=user.agent.organisation)
            # filter for the agent that is logged in
            queryset = queryset.filter(lead__agent__user=user)

        return queryset

    def get_success_url(self):
        return reverse("leads:lead-details", kwargs={"pk": self.get_object().lead.id})


class FollowUpDelete(OrganiserAndLoginMixin, DeleteView):
    template_name = "leads/followup_delete.html"

    def get_success_url(self):
        followup = FollowUp.objects.get(id=self.kwargs["pk"])
        return reverse("leads:lead-details", kwargs={"pk": followup.lead.pk})

    def get_queryset(self):
        user = self.request.user
        # initial queryset of leads for the entire organisation
        if user.is_organiser:
            queryset = FollowUp.objects.filter(
                lead__organisation=user.userprofile)
        else:
            queryset = FollowUp.objects.filter(
                lead__organisation=user.agent.organisation)
            # filter for the agent that is logged in
            queryset = queryset.filter(lead__agent__user=user)
        return queryset
