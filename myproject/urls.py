from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from . import global_utils
from . import settings

import json


urlpatterns = [
    path('admin/', admin.site.urls),

    path('mainapp/', include('mainapp.urls')),
    path('products/', include('products.urls')),
    path('company/', include('usercompany.urls')),
    path('customer/', include('usercustomer.urls')),
    path('courier/', include('usercourier.urls')),
]

file_dir = settings.VUE_SRC_DIR / 'api' / 'apiUrlPatterns.json'
url_data = global_utils.ParseUrlPatterns(settings.ROOT_URLCONF).parse_url_patterns()

with file_dir.open('w', encoding='utf-8') as f:
    json.dump(url_data, f, indent=4)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
