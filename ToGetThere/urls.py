from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^ToGetThere/', include('togetthereApp.urls', namespace="ToGetThere")),
    url(r'^admin/', include(admin.site.urls))
]
