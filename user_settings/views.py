from django.views.generic import FormView
from django.urls import reverse_lazy

from .forms import ChangePasswordForm


# Create your views here.

class UserSettingsView(FormView):
    template_name = 'user_settings/user_settings.html'
    form_class = ChangePasswordForm
    success_url = reverse_lazy('user_settings')

    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['default_password'] = 'SomeRandomPassword123'
        return context

