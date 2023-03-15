from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path

# Import views
from django.views.generic import TemplateView

app_name = 'authentication'
urlpatterns = [
    path('payment-api/login', TemplateView.as_view(template_name='authentication/index.html'), name='login'),
    path('payment-api/login/confirm-otp', TemplateView.as_view(template_name='authentication/confirm_otp.html'), name='enter-otp'),
]

urlpatterns += staticfiles_urlpatterns()