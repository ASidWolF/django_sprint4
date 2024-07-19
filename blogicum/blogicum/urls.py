from debug_toolbar.toolbar import debug_toolbar_urls
from django.conf import settings
from django.conf.urls import handler403, handler404, handler500
from django.conf.urls.static import static
from django.contrib import admin
# from django.contrib.auth import views as auth_views
# from django.contrib.auth.forms import (
#     PasswordChangeForm, PasswordResetForm
# )
from django.urls import include, path, reverse_lazy
from django.views.generic import CreateView

from core.forms import CustomUserCreationForm

handler403 = 'pages.views.custom_permission_denied'
handler404 = 'pages.views.custom_page_not_found'
handler500 = 'pages.views.custom_server_error'

urlpatterns = [
    path('', include('blog.urls', namespace='blog')),
    path('pages/', include('pages.urls', namespace='pages')),
    path('admin/', admin.site.urls),
    path('auth/', include('django.contrib.auth.urls')),
    path(
        'auth/registration/',
        CreateView.as_view(
            template_name='registration/registration_form.html',
            form_class=CustomUserCreationForm,
            success_url=reverse_lazy('blog:index'),
        ),
        name='registration',
    ),
    # path('__debug__/', include('debug_toolbar.urls')),
] + static(
    settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
)  # + debug_toolbar_urls()
