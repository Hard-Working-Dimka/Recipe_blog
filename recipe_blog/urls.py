from django.contrib import admin
from django.contrib.auth.views import LogoutView, PasswordResetView, PasswordResetConfirmView, PasswordResetDoneView, \
    PasswordResetCompleteView
from django.urls import path
from django.conf.urls.static import static

from recepies import views
from recepies.views import show_index, show_card, show_order
from recipe_blog import settings

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('', show_index, name='index'),
                  path('recipe/<slug:slug>/', show_card, name='show_card'),
                  path('order/', show_order, name='order'),
                  path('payment-confirm/<int:order_id>/', views.payment_confirm, name='payment_confirm'),
                  path('payment-success/<int:order_id>/', views.payment_success, name='payment_success'),
                  path('profile/', views.ProfileUser.as_view(), name='profile'),

                  path('login/', views.LoginUser.as_view(), name='login'),
                  path('logout/', LogoutView.as_view(), name='logout'),
                  path('register/', views.register, name='register'),

                  path('password_reset/', PasswordResetView.as_view(), name='password_reset'),
                  path('password_reset/done/', PasswordResetDoneView.as_view(), name='password_reset_done'),
                  path('reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(),
                       name='password_reset_confirm'),
                  path('reset/done/', PasswordResetCompleteView.as_view(), name='password_reset_complete'),

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_URL)

