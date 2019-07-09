from rest_framework.routers import DefaultRouter
from .views import *

urlpatterns = []

router = DefaultRouter()
router.register('areas', AreasViewSet, base_name='areas')



urlpatterns += router.urls