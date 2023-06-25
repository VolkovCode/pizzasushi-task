from django.urls import path, include, re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework.routers import DefaultRouter
from rest_framework import permissions
from .views import (
    BalanceViewSet,
    ReplenishmentViewSet, 
    DebitingViewSet,
    TransferViewSet
)

router_v1 = DefaultRouter()
router_v1.register(
    'balance',
    BalanceViewSet, basename='balance'
)

router_v1.register(
    'replenishment',
    ReplenishmentViewSet, basename='replenishment'
)
router_v1.register(
    'debiting',
    DebitingViewSet, basename='debiting'
)
router_v1.register(
    'transfer',
    TransferViewSet, basename='transfer'
)

urlpatterns = [
    path('', include(router_v1.urls)),
]

schema_view = get_schema_view(
   openapi.Info(
      title="API",
      default_version='v1',
      description="Документация приложения ",
      contact=openapi.Contact(email="alexeyvolkovspb97@gmail.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns += [
   re_path(r'^swagger(?P<format>\.json|\.yaml)$', 
       schema_view.without_ui(cache_timeout=0), name='schema-json'),
   re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), 
       name='schema-swagger-ui'),
   re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), 
       name='schema-redoc'),
]
