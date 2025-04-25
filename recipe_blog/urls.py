from django.contrib import admin
from django.contrib.auth.views import LogoutView, PasswordResetView, PasswordResetConfirmView, PasswordResetDoneView, \
    PasswordResetCompleteView
from django.urls import path
from django.conf.urls.static import static

from recepies import views
from recepies.views import show_index, show_card
from recipe_blog import settings

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('', show_index, name='index'),
                  path('recipe/<slug:slug>/', show_card, name='recipe_detail'),
                  # path('order/', show_order),
                  # path('profile/', show_lk, name='profile'),
                  path('profile/', views.ProfileUser.as_view(), name='profile'),

                  path('login/', views.LoginUser.as_view(), name='login'),
                  path('logout/', LogoutView.as_view(), name='logout'),
                  path('register/', views.register, name='register'),

                  path('password_reset/', PasswordResetView.as_view(), name='password_reset'),
                  path('password_reset/done/', PasswordResetDoneView.as_view(), name='password_reset_done'),
                  path('reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(),
                       name='password_reset_confirm'),
                  path('reset/done/', PasswordResetCompleteView.as_view(), name='password_reset_complete'),

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
