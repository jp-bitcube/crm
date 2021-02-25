from django.views.generic import TemplateView, CreateView
from django.shortcuts import reverse
from .forms import CustomUserCreationForm


class SignUp(CreateView):
    template_name = 'registration/sign_up.html'
    form_class = CustomUserCreationForm

    def get_success_url(self):
        return reverse("login")


class LandingPageView(TemplateView):
    template_name = 'landing_page.html'
