from  django.conf.urls import url
from rest_framework.routers import DefaultRouter

from .views import *

urlpatterns = [
    url(r'^categories/(?P<category_id>\d+)/skus/', SKUListView.as_view())
]

router =DefaultRouter()
router.register('skus/search',SKUSearchViewSet,base_name='skus_search')

urlpatterns += router.urls