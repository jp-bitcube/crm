from django.shortcuts import reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import CategoryForm, CategoryForm2
from agents.mixins import OrganiserAndLoginMixin
from leads.models import Lead, Category
# Create your views here.


class CategoriesList(LoginRequiredMixin, ListView):
    template_name = 'category/category_list.html'
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
    template_name = 'category/category_create.html'
    form_class = CategoryForm2

    def get_success_url(self):
        return reverse("category:category-list")

    def form_valid(self, form):
        category = form.save(commit=False)
        category.organisation = self.request.user.userprofile
        category.save()
        return super(CategoriesCreate, self).form_valid(form)


class CategoriesUpdate(OrganiserAndLoginMixin, UpdateView):
    template_name = 'category/category_update.html'
    form_class = CategoryForm2

    def get_success_url(self):
        return reverse("category:category-list")

    def get_queryset(self):
        user = self.request.user
        if user.is_organiser:
            queryset = Category.objects.filter(
                organisation=user.userprofile)

        return queryset


class CategoriesDelete(OrganiserAndLoginMixin, DeleteView):
    template_name = 'category/category_delete.html'

    def form_valid(self, form):
        user = self.request.user
        category = Category.objects.get(id=pk)
        category.delete()
        return super(CategoriesDelete, self).form_valid(form)

    def get_success_url(self):
        return reverse("category:category-list")

    def get_queryset(self):
        user = self.request.user
        if user.is_organiser:
            queryset = Category.objects.filter(
                organisation=user.userprofile)

        return queryset


class CategoriesDetails(LoginRequiredMixin, DetailView):
    template_name = 'category/category_details.html'
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
    template_name = 'category/lead_category_details.html'
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
