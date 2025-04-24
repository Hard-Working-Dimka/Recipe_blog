import django.contrib.admin
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static

from recipe_blog import settings
from recepies.views import show_index, show_auth, show_card, show_lk, show_order, RegisterUser

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('', show_index, name='index'),
                  path('authentication/', show_auth),
                  path('recipe/', show_card),  # <int:id>/
                  path('order/', show_order),
                  path('registration/', RegisterUser.as_view(), name='registration'),
                  path('accounts/', include('django.contrib.auth.urls')),

                path('accounts/profile/', show_lk),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
