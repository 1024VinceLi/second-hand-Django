from  django.conf.urls import url

from .views import *

urlpatterns = [
    url(r'^categories/(?P<category_id>\d+)/skus/', SKUListView.as_view())
]