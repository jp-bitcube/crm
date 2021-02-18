from django.shortcuts import render, redirect, reverse
from django.core.mail import send_mail
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView, FormView
from .models import Lead, Agent
from .forms import LeadModelForm, LeadForm, CustomUserCreationForm, AssignAgentForm
from agents.mixins import OrganiserAndLoginMixin


class SignUp(CreateView):
    template_name = 'registration/sign_up.html'
    form_class = CustomUserCreationForm

    def get_success_url(self):
        return reverse("login")


class LandingPageView(TemplateView):
    template_name = 'landing_page.html'


def landing_page(request):
    return render(request, 'landing_page.html')


class LeadList(LoginRequiredMixin, ListView):
    template_name = 'leads/lead_list.html'
    context_object_name = 'leads'

    def get_queryset(self):
        user = self.request.user
        if self.request.user.is_organiser:
            queryset = Lead.objects.filter(
                organisation=user.agent.organisation, agent__isnull=False)
        else:
            queryset = Lead.objects.filter(
                organisation=user.userprofile, agent__isnull=False)
            queryset = queryset.filter(agent__user=user)
        return queryset

    def get_context_data(self, **kwargs):
        user = self.request.user
        context = super(LeadList, self).get_context_data(**kwargs)
        if user.is_organiser:
            queryset = Lead.objects.filter(
                organisation=user.agent.organisation, agent__isnull=True)
            context.update({
                "unassigned_leads": queryset
            })
        return context


def lead_list(request):
    leads = Lead.objects.all()
    context = {"leads": leads}
    return render(request, "leads/lead_list.html", context)


class LeadDetails(LoginRequiredMixin, DetailView):
    template_name = 'leads/lead_details.html'
    context_object_name = 'lead'

    def get_queryset(self):
        user = self.request.user
        if self.request.user.is_organiser:
            queryset = Lead.objects.filter(
                organisation=user.agent.organisation)
        else:
            queryset = Lead.objects.filter(
                organisation=user.userprofile)
            queryset = queryset.filter(agent__user=user)
        return queryset


def lead_details(request, pk):
    lead = Lead.objects.get(id=pk)
    context = {"lead": lead}
    return render(request, "leads/lead_details.html", context)


class LeadCreate(OrganiserAndLoginMixin, CreateView):
    template_name = 'leads/lead_create.html'
    form_class = LeadModelForm

    def get_success_url(self):
        return reverse("leads:lead-list")

    def form_valid(self, form):
        lead = form.save(commit=False)
        lead.organisation = self.request.user.userprofile
        lead.save()
        send_mail(
            subject="Lead has been created",
            message="Go to site to view the lead",
            from_email="test@test.com",
            recipient_list=["Test@test2.com"]
        )
        return super(LeadCreate, self).form_valid(form)


def lead_create(request):
    form = LeadModelForm()
    if request.method == 'POST':
        form = LeadModelForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("/leads")
    context = {"form": form}
    return render(request, "leads/lead_create.html", context)


class LeadUpdate(OrganiserAndLoginMixin, UpdateView):
    template_name = 'leads/lead_update.html'
    form_class = LeadModelForm

    def get_queryset(self):
        user = self.request.user
        if self.request.user.is_organiser:
            queryset = Lead.objects.filter(
                organisation=user.agent.organisation)
        else:
            queryset = Lead.objects.filter(
                organisation=user.userprofile)
            queryset = queryset.filter(agent__user=user)
        return queryset

    def get_success_url(self):
        return reverse("leads:lead-list")


def lead_update(request, pk):
    lead = Lead.objects.get(id=pk)
    form = LeadModelForm(instance=lead)
    if request.method == 'POST':
        form = LeadModelForm(request.POST, instance=lead)
        if form.is_valid():
            form.save()
            return redirect("/leads")
    context = {
        "lead": lead,
        "form": form
    }
    return render(request, "leads/lead_update.html", context)


class LeadDelete(OrganiserAndLoginMixin, DeleteView):
    template_name = 'leads/lead_delete.html'

    def get_queryset(self):
        user = self.request.user
        if self.request.user.is_organiser:
            queryset = Lead.objects.filter(
                organisation=user.agent.organisation)
        else:
            queryset = Lead.objects.filter(
                organisation=user.userprofile)
            queryset = queryset.filter(agent__user=user)
        return queryset

    def get_success_url(self):
        return reverse("leads:lead-list")


def lead_delete(request, pk):
    lead = Lead.objects.get(id=pk)
    lead.delete()
    return redirect("/leads")


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
