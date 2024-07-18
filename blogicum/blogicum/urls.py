from debug_toolbar.toolbar import debug_toolbar_urls
from django.conf import settings
from django.conf.urls import handler403, handler404, handler500
from django.conf.urls.static import static
from django.contrib import admin
# from django.contrib.auth import views as auth_views
# from django.contrib.auth.forms import (
#     PasswordChangeForm, PasswordResetForm
# )
from django.urls import include, path  # , reverse_lazy
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
        'registration/',
        CreateView.as_view(
            form_class=CustomUserCreationForm,
            success_url='/',
            template_name='registration/registration_form.html',
        ),
        name='registration'
    ),
    # path('__debug__/', include('debug_toolbar.urls')),
] + debug_toolbar_urls() + static(
    settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
)

# auth_urls = ([
#     path(
#         'login/',
#         auth_views.LoginView.as_view(
#             template_name='registration/login.html'
#         ),
#         name='login',
#     ),
#     path(
#         'logout/',
#         auth_views.LogoutView.as_view(
#             template_name='registration/logged_out.html'
#         ),
#         name='logout',
#     ),
#     path(
#         'registration/',
#         CreateView.as_view(
#             form_class=CustomUserCreationForm,
#             success_url='/',
#             template_name='registration/registration_form.html',
#         ),
#         name='registration'
#     ),
#     path(
#         'password_change/',
#         auth_views.PasswordChangeView.as_view(
#             form_class=PasswordChangeForm,
#             success_url=reverse_lazy('users:password_change_done'),
#             template_name='registration/password_change_form.html',
#         ),
#         name='password_change'
#     ),
#     path(
#         'password_change_done/',
#         auth_views.PasswordChangeDoneView.as_view(
#             template_name='registration/password_change_done.html',
#         ),
#         name='password_change_done'
#     ),
#     path(
#         'password_reset/',
#         auth_views.PasswordResetView.as_view(
#             form_class=PasswordResetForm,
#             email_template_name='registration/password_reset_email.html',
#             success_url=reverse_lazy('users:password_reset_done'),
#             template_name='registration/password_reset_form.html',
#         ),
#         name='password_reset'
#     ),
#     path(
#         'password_reset_done/',
#         auth_views.PasswordResetDoneView.as_view(
#             template_name='registration/password_reset_done.html',
#         ),
#         name='password_reset_done'
#     ),
#     path(
#         'password_reset_confirm/<uidb64>/<token>/',
#         auth_views.PasswordResetConfirmView.as_view(
#             template_name='registration/password_reset_confirm.html',
#             success_url=reverse_lazy('users:password_reset_complete')
#         ),
#         name='password_reset_confirm'
#     ),
#     path(
#         'password_reset_complete/',
#         auth_views.PasswordResetCompleteView.as_view(
#             template_name='registration/password_reset_complete.html'
#         ), name='password_reset_complete'
#     ),
# ], 'users')

# urlpatterns += [path('auth/', include(auth_urls))]
