
from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('',include('app.urls')),
    path('erp/',include('erp_app.urls')),
    path('admin/', admin.site.urls),
]
