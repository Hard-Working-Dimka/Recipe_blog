import django.contrib.admin
from django.contrib import admin
from django.contrib.auth.views import LogoutView, PasswordChangeView, PasswordChangeDoneView, PasswordResetDoneView, \
    PasswordResetView, PasswordResetConfirmView
from django.urls import path, include
from django.conf.urls.static import static

from recepies import views
from recepies.views import show_index, show_lk
from recipe_blog import settings

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('', show_index, name='index'),
                  # path('recipe/', show_card),  # <int:id>/
                  # path('order/', show_order),
                  # path('accounts/', include('django.contrib.auth.urls')),

                  path('login/', views.LoginUser.as_view(), name='login'),
                  path('logout/', LogoutView.as_view(), name='logout'),
                  path('register/', views.register, name='register'),

                  path('password-reset/', PasswordResetView.as_view(), name='password_reset'),
                  path('password_reset/done/', PasswordResetView.as_view(), name='password_reset_done'),
                  path('password-reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(),
                       name='password_reset_confirm'),

                  path('profile/', show_lk, name='profile'),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
