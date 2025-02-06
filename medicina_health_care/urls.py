from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from django.urls import path,include


urlpatterns = [
    path('admin/', admin.site.urls),

    path('user/', include('user_app.urls')),
    path('cart/', include('cart_app.urls')),
    path('product/', include('product_app.urls'))


]



# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)