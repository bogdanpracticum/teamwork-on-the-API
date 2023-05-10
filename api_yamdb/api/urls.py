from rest_framework import routers
from django.urls import include, path

app_name = 'api'


router_v1 = routers.DefaultRouter()


urlpatterns = [
    path('v1/', include(router_v1.urls)),
]
