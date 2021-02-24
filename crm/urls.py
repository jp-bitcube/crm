from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth.views import (
    LoginView, LogoutView,
    PasswordResetView, PasswordResetDoneView,
    PasswordResetConfirmView, PasswordResetCompleteView
)
from django.urls import path, include
from leads.views import LandingPageView, SignUp

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', LandingPageView.as_view(), name='landing_page'),
    path('leads/', include('leads.urls', namespace="leads")),
    path('agents/', include('agents.urls', namespace="agents")),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('signup/', SignUp.as_view(), name='sign_up'),
    path('reset_password/', PasswordResetView.as_view(
        html_email_template_name='registration/password_reset_html_email.html'
    ), name='reset_password'),
    path('password_reset_complete/', PasswordResetCompleteView.as_view(),
         name='password_reset_complete'),
    path('password_reset_confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(),
         name='password_reset_confirm'),
    path('password_reset_done/', PasswordResetDoneView.as_view(),
         name='password_reset_done')
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
