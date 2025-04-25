from django.contrib import admin
from django.contrib.auth.views import LogoutView, PasswordResetView, PasswordResetConfirmView
from django.urls import path
from django.conf.urls.static import static

from recepies import views
from recepies.views import show_index, show_lk, show_card
from recipe_blog import settings

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('', show_index, name='index'),
                  path('recipe/<slug:slug>/', show_card, name='recipe_detail'),
                  # path('order/', show_order),
                  # path('accounts/', include('django.contrib.auth.urls')),

                  path('login/', views.LoginUser.as_view(), name='login'),
                  path('logout/', LogoutView.as_view(), name='logout'),
                  path('register/', views.register, name='register'),

                  # TODO: нормально не работает, посмотреть
                  path('password-reset/', PasswordResetView.as_view(), name='password_reset'),
                  path('password_reset/done/', PasswordResetView.as_view(), name='password_reset_done'),
                  path('password-reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(),
                       name='password_reset_confirm'),

                  path('profile/', show_lk, name='profile'),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)