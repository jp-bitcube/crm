from django.shortcuts import render, redirect, reverse
from django.core.mail import send_mail
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView, FormView
from .models import Lead, Agent, Category
from .forms import LeadModelForm, LeadForm, CustomUserCreationForm, AssignAgentForm, CategoryForm, CategoryForm2
from agents.mixins import OrganiserAndLoginMixin


class SignUp(CreateView):
    template_name = 'registration/sign_up.html'
    form_class = CustomUserCreationForm

    def get_success_url(self):
        return reverse("login")


class LandingPageView(TemplateView):
    template_name = 'landing_page.html'


class LeadList(LoginRequiredMixin, ListView):
    template_name = 'leads/lead_list.html'
    context_object_name = 'leads'

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
        print(lead)
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


class CategoriesList(LoginRequiredMixin, ListView):
    template_name = 'leads/category_list.html'
    context_object_name = 'categories'
    count = 'count'

    def get_context_data(self, **kwargs):
        user = self.request.user
        context = super(CategoriesList, self).get_context_data(**kwargs)
        if user.is_organiser:
            queryset = Lead.objects.filter(
                organisation=user.userprofile)
            categories = Category.objects.filter(
                organisation=user.userprofile)
        else:
            queryset = Lead.objects.filter(
                organisation=user.agent.organisation)
            categories = Category.objects.filter(
                organisation=user.agent.organisation)

        cats = []
        for category in categories:
            cats.append({
                "category": {
                    "pk": category.id,
                    "name": category.name,
                    "count": queryset.filter(category_id=category.id).count()
                }
            })
        if len(cats) == len(categories):
            context.update({
                "unassigned_lead_count": queryset.filter(category__isnull=True).count(),
                "categories": cats
            })
            return context

    def get_queryset(self):
        user = self.request.user
        if user.is_organiser:
            queryset = Category.objects.filter(
                organisation=user.userprofile)
        else:
            queryset = Category.objects.filter(
                organisation=user.agent.organisation)
        return queryset


class CategoriesCreate(OrganiserAndLoginMixin, CreateView):
    template_name = 'leads/category_create.html'
    form_class = CategoryForm2

    def get_success_url(self):
        return reverse("leads:category-list")

    def form_valid(self, form):
        category = form.save(commit=False)
        category.organisation = self.request.user.userprofile
        category.save()
        return super(CategoriesCreate, self).form_valid(form)


class CategoriesUpdate(OrganiserAndLoginMixin, UpdateView):
    template_name = 'leads/category_update.html'
    form_class = CategoryForm2

    def get_success_url(self):
        return reverse("leads:category-list")

    def get_queryset(self):
        user = self.request.user
        if user.is_organiser:
            queryset = Category.objects.filter(
                organisation=user.userprofile)

        return queryset


class CategoriesDelete(OrganiserAndLoginMixin, DeleteView):
    template_name = 'leads/category_delete.html'

    def form_valid(self, form):
        user = self.request.user
        category = Category.objects.get(id=pk)
        print(category)
        category.delete()
        return super(CategoriesDelete, self).form_valid(form)

    def get_success_url(self):
        return reverse("leads:category-list")

    def get_queryset(self):
        user = self.request.user
        if user.is_organiser:
            queryset = Category.objects.filter(
                organisation=user.userprofile)

        return queryset


class CategoriesDetails(LoginRequiredMixin, DetailView):
    template_name = 'leads/category_details.html'
    context_object_name = 'category'

    def get_context_data(self, **kwargs):
        user = self.request.user
        context = super(CategoriesDetails, self).get_context_data(**kwargs)
        leads = self.get_object().leads.all()
        context.update({
            "leads": leads
        })
        return context

    def get_queryset(self):
        user = self.request.user
        if user.is_organiser:
            queryset = Category.objects.filter(
                organisation=user.userprofile)
        else:
            queryset = Category.objects.filter(
                organisation=user.agent.organisation)
        return queryset


class CategoryLeadUpdate(LoginRequiredMixin, UpdateView):
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
