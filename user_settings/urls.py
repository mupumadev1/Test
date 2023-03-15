from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path

# Import views
from .views import UserSettingsView

app_name = 'user_settings'
urlpatterns = [
    path('payments-api/user-settings', UserSettingsView.as_view(), name='user_settings'),
]

urlpatterns += staticfiles_urlpatterns()