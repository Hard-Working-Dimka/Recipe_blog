from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static

from recipe_blog import settings
from recepies.views import show_index, show_auth, show_card, show_lk, show_order, show_registration

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('', show_index),
                  path('authentication/', show_auth),
                  path('recipe/<slug:slug>/', show_card, name='recipe_detail'),
                  path('lk/', show_lk), #<int:id>/ TODO: добавить после моделей!
                  path('order/', show_order),
                  path('registration/', show_registration),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
