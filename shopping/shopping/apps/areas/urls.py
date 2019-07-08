from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r'areas', AreasViewSet, base_name='areas')

urlpatterns = []

urlpatterns += router.urls